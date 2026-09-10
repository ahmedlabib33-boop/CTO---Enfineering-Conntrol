\
from __future__ import annotations
from pathlib import Path
from uuid import uuid4
from hashlib import sha256
from datetime import datetime
import json, mimetypes, shutil

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import select

from .config import UPLOAD_DIR, OUTPUT_DIR, EXPORT_DIR, MAX_UPLOAD_MB, DEMO_ADMIN_USER, DEMO_ADMIN_PASSWORD, DEMO_TOKEN, CORS_ORIGINS
from .db import init_db, SessionLocal, Project, Document, DrawingParse, ComparisonRun, Change, QaRun, ExportRecord, AuditEvent
from .schemas import LoginRequest, ProjectCreate, ComparisonCreate, ModificationCreate, QaCreate, ExportCreate, MlFeedback, MlTrainRequest, MathSymbolicRequest, MlWorkbenchTrainRequest, MlWorkbenchPredictRequest, MlUnsupervisedRequest, MathStatsRequest, PlanningDurationRequest, PlanningProcurementRequest, PlanningScheduleQARequest, PlanningReviewRequest, PlanningXerRequest, PlanningMLTrainRequest, PlanningMLPredictRequest, PlanningAnomalyRequest
from .services.cad import parse_dxf, apply_changes
from .services.comparison import compare_entities
from .services.qa import run_qa
from .services.exports import dxf_to_pdf, redline_pdf, change_register_xlsx
from .services.ml import AdaptiveChangeClassifier, EngineeringMathEngine, StatisticsMathEngine, TabularMLWorkbench, UnsupervisedEngineeringML, capability_report
from .services.ml.features import change_features
from .config import ML_DIR, KNOWLEDGE_DIR, KNOWLEDGE_INDEX_DIR
from .services.ml.knowledge_index import EngineeringKnowledgeIndex
from .services.planning import pipeline_definition, DurationEngine, ProcurementEngine, ScheduleQAEngine, ScheduleBasisEngine, ConstructabilityEngine, XerCreator, PlanningMLHub

app = FastAPI(title="Engineering CAD Platform API", version="0.1.0")

# Frontend and backend deploy to separate origins (e.g. a Vercel-hosted
# Next.js app calling a backend hosted elsewhere), so the browser needs
# explicit CORS clearance. allow_credentials stays False because auth here
# is a manually-set Authorization header, not browser-managed cookies —
# that also keeps CORS_ORIGINS=["*"] valid (the two are mutually exclusive
# per the CORS spec).
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()
    sources=[p for p in KNOWLEDGE_DIR.iterdir() if p.is_file() and p.suffix.lower() in {'.md','.txt','.html'}]
    if sources:
        idx=EngineeringKnowledgeIndex(KNOWLEDGE_INDEX_DIR)
        newest=max(p.stat().st_mtime for p in sources)
        if (not idx.bundle_path.exists()) or idx.bundle_path.stat().st_mtime < newest:
            idx.build(sources)

def auth(authorization: str | None):
    if authorization != f"Bearer {DEMO_TOKEN}":
        raise HTTPException(status_code=401, detail="Invalid or missing bearer token")

def audit(db, action, target="", result="OK", project_id=None):
    db.add(AuditEvent(project_id=project_id, action=action, target=str(target), result=result))
    db.commit()

@app.get("/health")
def health():
    return {"status":"healthy"}

@app.post("/auth/login")
def login(payload: LoginRequest):
    if payload.username == DEMO_ADMIN_USER and payload.password == DEMO_ADMIN_PASSWORD:
        return {"access_token":DEMO_TOKEN,"token_type":"bearer","role":"Admin"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/projects")
def create_project(payload: ProjectCreate, authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        p=Project(name=payload.name); db.add(p); db.commit(); db.refresh(p)
        audit(db,"project.create",p.id,project_id=p.id)
        return {"id":p.id,"name":p.name,"created_at":p.created_at}

@app.get("/projects")
def list_projects(authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        rows=db.scalars(select(Project).order_by(Project.id.desc())).all()
        return [{"id":r.id,"name":r.name,"created_at":r.created_at} for r in rows]

@app.post("/projects/{project_id}/documents")
async def upload_document(project_id: int, file: UploadFile = File(...), kind: str = Form("drawing"),
                          revision: str = Form(""), authorization: str | None = Header(default=None)):
    auth(authorization)
    ext=Path(file.filename or "").suffix.lower()
    allowed={".dxf",".pdf",".ifc",".txt",".md",".csv",".xlsx",".docx",".png",".jpg",".jpeg",".tiff",".svg"}
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported extension: {ext}")
    data=await file.read()
    if len(data) > MAX_UPLOAD_MB*1024*1024:
        raise HTTPException(status_code=413, detail="File exceeds configured upload limit")
    digest=sha256(data).hexdigest()
    stored=UPLOAD_DIR / f"{project_id}_{uuid4().hex}{ext}"
    stored.write_bytes(data)
    with SessionLocal() as db:
        if not db.get(Project, project_id):
            stored.unlink(missing_ok=True)
            raise HTTPException(status_code=404, detail="Project not found")
        doc=Document(project_id=project_id, original_name=file.filename or stored.name, stored_path=str(stored),
                     sha256=digest, mime_type=file.content_type or mimetypes.guess_type(file.filename or "")[0] or "application/octet-stream",
                     kind=kind, revision=revision)
        db.add(doc); db.commit(); db.refresh(doc)
        audit(db,"document.upload",doc.id,project_id=project_id)
        return {"id":doc.id,"project_id":project_id,"filename":doc.original_name,"sha256":doc.sha256,"revision":doc.revision}

@app.get("/projects/{project_id}/documents")
def list_documents(project_id: int, authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        rows=db.scalars(select(Document).where(Document.project_id==project_id).order_by(Document.id)).all()
        return [{"id":r.id,"filename":r.original_name,"kind":r.kind,"revision":r.revision,"sha256":r.sha256} for r in rows]

@app.post("/drawings/{document_id}/parse")
def parse_drawing(document_id: int, authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        doc=db.get(Document, document_id)
        if not doc: raise HTTPException(404,"Document not found")
        if Path(doc.stored_path).suffix.lower() != ".dxf":
            raise HTTPException(400,"MVP parser currently requires DXF")
        result=parse_dxf(doc.stored_path)
        row=DrawingParse(document_id=document_id,
            summary_json=json.dumps({k:v for k,v in result.items() if k!="entities"}),
            entities_json=json.dumps(result["entities"]))
        db.add(row); db.commit(); db.refresh(row)
        audit(db,"drawing.parse",document_id,project_id=doc.project_id)
        return {"parse_id":row.id, **{k:v for k,v in result.items() if k!="entities"}, "entities":result["entities"]}

@app.post("/comparison-runs")
def create_comparison(payload: ComparisonCreate, authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        cur=db.get(Document,payload.current_document_id); ref=db.get(Document,payload.reference_document_id)
        if not cur or not ref: raise HTTPException(404,"Drawing document not found")
        if cur.project_id != payload.project_id or ref.project_id != payload.project_id:
            raise HTTPException(400,"Documents must belong to the project")
        cur_parsed=parse_dxf(cur.stored_path); ref_parsed=parse_dxf(ref.stored_path)
        run=ComparisonRun(project_id=payload.project_id,current_document_id=cur.id,reference_document_id=ref.id)
        db.add(run); db.commit(); db.refresh(run)
        changes=compare_entities(cur_parsed["entities"],ref_parsed["entities"])
        for c in changes:
            db.add(Change(comparison_id=run.id, change_key=c["change_key"], change_type=c["change_type"],
                change_class=c["change_class"], authority=c["authority"], source_handle=c["source_handle"],
                target_handle=c["target_handle"], before_json=json.dumps(c["before"]), after_json=json.dumps(c["after"]),
                confidence=c["confidence"], status=c["status"]))
        db.commit()
        audit(db,"comparison.run",run.id,project_id=payload.project_id)
        return {"id":run.id,"change_count":len(changes),"changes":changes}

@app.get("/comparison-runs/{comparison_id}/changes")
def get_changes(comparison_id: int, authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        rows=db.scalars(select(Change).where(Change.comparison_id==comparison_id).order_by(Change.id)).all()
        return [_change_out(r) for r in rows]

def _change_out(r):
    return {"id":r.id,"change_key":r.change_key,"change_type":r.change_type,"change_class":r.change_class,
            "authority":r.authority,"source_handle":r.source_handle,"target_handle":r.target_handle,
            "before":json.loads(r.before_json),"after":json.loads(r.after_json),"confidence":r.confidence,"status":r.status}

@app.post("/changes/{change_id}/approve")
def approve_change(change_id: int, authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        c=db.get(Change,change_id)
        if not c: raise HTTPException(404,"Change not found")
        if c.change_class == "C":
            c.status="ENGINEERING_REVIEW_REQUIRED"; db.commit()
            raise HTTPException(status_code=409, detail="Class C cannot be auto-approved; engineering approval required")
        c.status="APPROVED"; db.commit()
        run=db.get(ComparisonRun,c.comparison_id)
        audit(db,"change.approve",c.change_key,project_id=run.project_id if run else None)
        return _change_out(c)

@app.post("/changes/{change_id}/reject")
def reject_change(change_id: int, authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        c=db.get(Change,change_id)
        if not c: raise HTTPException(404,"Change not found")
        c.status="REJECTED"; db.commit()
        return _change_out(c)

@app.post("/changes/{change_id}/hold")
def hold_change(change_id: int, authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        c=db.get(Change,change_id)
        if not c: raise HTTPException(404,"Change not found")
        c.status="HOLD"; db.commit()
        return _change_out(c)

@app.post("/modification-runs")
def modify(payload: ModificationCreate, authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        run=db.get(ComparisonRun,payload.comparison_id)
        if not run: raise HTTPException(404,"Comparison not found")
        current=db.get(Document,run.current_document_id); reference=db.get(Document,run.reference_document_id)
        rows=db.scalars(select(Change).where(Change.comparison_id==run.id).order_by(Change.id)).all()
        changes=[_change_out(r) for r in rows]
        out=OUTPUT_DIR / f"project_{run.project_id}_comparison_{run.id}_revised.dxf"
        apply_changes(current.stored_path,reference.stored_path,changes,out)
        qa=run_qa(out)
        audit(db,"modification.apply",out.name,project_id=run.project_id)
        return {"comparison_id":run.id,"revised_dxf_path":str(out),"qa":qa}

@app.post("/qa-runs")
def qa_run(payload: QaCreate, authorization: str | None = Header(default=None)):
    auth(authorization)
    result=run_qa(payload.file_path)
    with SessionLocal() as db:
        row=QaRun(project_id=payload.project_id,file_path=payload.file_path,status=result["status"],result_json=json.dumps(result))
        db.add(row); db.commit(); db.refresh(row)
        audit(db,"qa.run",row.id,project_id=payload.project_id)
        return {"id":row.id,**result}

@app.post("/exports")
def create_exports(payload: ExportCreate, authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        run=db.get(ComparisonRun,payload.comparison_id)
        if not run: raise HTTPException(404,"Comparison not found")
        rows=db.scalars(select(Change).where(Change.comparison_id==run.id).order_by(Change.id)).all()
        changes=[_change_out(r) for r in rows]
        base=EXPORT_DIR / f"project_{payload.project_id}_comparison_{payload.comparison_id}"
        pdf=dxf_to_pdf(payload.revised_dxf_path, str(base)+"_revised.pdf")
        red=redline_pdf(changes, str(base)+"_redline.pdf")
        xlsx=change_register_xlsx(changes, str(base)+"_change_register.xlsx")
        outputs={"dxf":payload.revised_dxf_path,"pdf":pdf,"redline":red,"change_register":xlsx}
        ids={}
        for typ,path in outputs.items():
            rec=ExportRecord(project_id=payload.project_id,export_type=typ,file_path=path)
            db.add(rec); db.commit(); db.refresh(rec); ids[typ]=rec.id
        audit(db,"export.create",payload.comparison_id,project_id=payload.project_id)
        return {"exports":outputs,"ids":ids}

@app.get("/exports/{export_id}/download")
def download_export(export_id: int, authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        rec=db.get(ExportRecord,export_id)
        if not rec: raise HTTPException(404,"Export not found")
        p=Path(rec.file_path)
        if not p.exists(): raise HTTPException(404,"Export file missing")
        audit(db,"export.download",export_id,project_id=rec.project_id)
        return FileResponse(p, filename=p.name)
\

@app.get("/ml/capabilities")
def ml_capabilities(authorization: str | None = Header(default=None)):
    auth(authorization)
    return capability_report()

@app.post("/ml/feedback")
def ml_feedback(payload: MlFeedback, authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        c=db.get(Change,payload.change_id)
        if not c: raise HTTPException(404,"Change not found")
        run=db.get(ComparisonRun,c.comparison_id)
        if not run or run.project_id != payload.project_id:
            raise HTTPException(400,"Change does not belong to project")
        change=_change_out(c)
        learner=AdaptiveChangeClassifier(ML_DIR,payload.project_id)
        rec=learner.record_reviewed_example(change,payload.reviewed_class,payload.reviewer)
        audit(db,"ml.feedback",c.change_key,project_id=payload.project_id)
        return {"status":"RECORDED","example":rec}

@app.post("/ml/train")
def ml_train(payload: MlTrainRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    learner=AdaptiveChangeClassifier(ML_DIR,payload.project_id)
    result=learner.train(payload.minimum_examples)
    with SessionLocal() as db:
        audit(db,"ml.train",result.get("status","UNKNOWN"),project_id=payload.project_id)
    return result

@app.get("/ml/predict-change/{change_id}")
def ml_predict_change(change_id: int, authorization: str | None = Header(default=None)):
    auth(authorization)
    with SessionLocal() as db:
        c=db.get(Change,change_id)
        if not c: raise HTTPException(404,"Change not found")
        run=db.get(ComparisonRun,c.comparison_id)
        change=_change_out(c)
        learner=AdaptiveChangeClassifier(ML_DIR,run.project_id)
        pred=learner.predict(change)
        # ML remains advisory. It cannot lower a deterministic Class C gate.
        pred["deterministic_class"]=c.change_class
        pred["deterministic_authority"]=c.authority
        if c.change_class == "C":
            pred["effective_authority"]="ENGINEERING_APPROVAL_REQUIRED"
        else:
            pred["effective_authority"]="HUMAN_REVIEW_REQUIRED"
        return pred

@app.get("/ml/training-history/{project_id}")
def ml_training_history(project_id: int, authorization: str | None = Header(default=None)):
    auth(authorization)
    learner=AdaptiveChangeClassifier(ML_DIR,project_id)
    history=learner.training_history()
    return {"project_id":project_id,"model_version":learner.model_version,"retrain_count":len(history),"history":history}

@app.post("/math/symbolic-check")
def math_symbolic(payload: MathSymbolicRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    return EngineeringMathEngine.symbolic_check(payload.expression,payload.substitutions)
\

@app.post("/knowledge/rebuild")
def knowledge_rebuild(authorization: str | None = Header(default=None)):
    auth(authorization)
    sources=[p for p in KNOWLEDGE_DIR.iterdir() if p.is_file() and p.suffix.lower() in {'.md','.txt','.html'}]
    if not sources: raise HTTPException(404,"Knowledge files not found")
    idx=EngineeringKnowledgeIndex(KNOWLEDGE_INDEX_DIR)
    return idx.build(sources)

@app.get("/knowledge/search")
def knowledge_search(q: str, k: int = 8, authorization: str | None = Header(default=None)):
    auth(authorization)
    idx=EngineeringKnowledgeIndex(KNOWLEDGE_INDEX_DIR)
    if not idx.bundle_path.exists():
        sources=[p for p in KNOWLEDGE_DIR.iterdir() if p.is_file() and p.suffix.lower() in {'.md','.txt','.html'}]
        if sources: idx.build(sources)
    return {"query":q,"authority":"GENERIC_REFERENCE_ONLY","results":idx.search(q,k)}


@app.post("/ml/workbench/train")
def ml_workbench_train(payload: MlWorkbenchTrainRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    try:
        return TabularMLWorkbench(ML_DIR / "workbench").train(
            payload.records, payload.target, payload.task, payload.model,
            payload.test_size, payload.cv_folds, payload.pca_components, payload.tune
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post("/ml/workbench/predict/{model_id}")
def ml_workbench_predict(model_id: str, payload: MlWorkbenchPredictRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    try:
        return TabularMLWorkbench(ML_DIR / "workbench").predict(model_id, payload.records)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model not found")

@app.post("/ml/unsupervised")
def ml_unsupervised(payload: MlUnsupervisedRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    try:
        if payload.method.lower()=="kmeans":
            return UnsupervisedEngineeringML.kmeans(payload.records,payload.clusters,payload.columns)
        if payload.method.lower()=="pca":
            return UnsupervisedEngineeringML.pca(payload.records,payload.components,payload.columns)
        raise HTTPException(status_code=400, detail="method must be kmeans or pca")
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post("/math/statistics")
def math_statistics(payload: MathStatsRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    op=payload.operation.lower()
    try:
        if op=="mean": return {"operation":op,"value":StatisticsMathEngine.mean(payload.values)}
        if op=="variance": return {"operation":op,"value":StatisticsMathEngine.variance(payload.values)}
        if op=="stddev": return {"operation":op,"value":StatisticsMathEngine.stddev(payload.values)}
        if op=="dot": return {"operation":op,"value":StatisticsMathEngine.dot(payload.values,payload.values_b)}
        if op=="covariance": return {"operation":op,"value":StatisticsMathEngine.covariance(payload.values,payload.values_b)}
        if op=="correlation": return {"operation":op,"value":StatisticsMathEngine.correlation(payload.values,payload.values_b)}
        if op=="conditional_probability": return {"operation":op,"value":StatisticsMathEngine.conditional_probability(payload.joint_count,payload.condition_count)}
        if op=="bayes": return {"operation":op,"value":StatisticsMathEngine.bayes_posterior(payload.prior,payload.likelihood,payload.evidence)}
        if op=="gradient_descent_linear_regression": return StatisticsMathEngine.gradient_descent_linear_regression(payload.values,payload.values_b)
        raise HTTPException(status_code=400, detail="Unsupported statistics operation")
    except (ValueError,TypeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# -----------------------------------------------------------------------------
# CONSTRUCTION PLANNING / PRIMAVERA INTELLIGENCE LAYER
# -----------------------------------------------------------------------------
@app.get("/planning/pipeline")
def planning_pipeline(authorization: str | None = Header(default=None)):
    auth(authorization)
    return pipeline_definition()

@app.post("/planning/duration/calculate")
def planning_duration(payload: PlanningDurationRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    try: return DurationEngine.calculate(**payload.model_dump())
    except ValueError as exc: raise HTTPException(status_code=400, detail=str(exc))

@app.post("/planning/procurement/analyze")
def planning_procurement(payload: PlanningProcurementRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    try: return ProcurementEngine.analyze(**payload.model_dump())
    except ValueError as exc: raise HTTPException(status_code=400, detail=str(exc))

@app.post("/planning/schedule/qa")
def planning_schedule_qa(payload: PlanningScheduleQARequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    return ScheduleQAEngine.review(payload.activities,payload.relationships,payload.excessive_lag_days)

@app.post("/planning/aace/schedule-basis")
def planning_schedule_basis(payload: PlanningReviewRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    return ScheduleBasisEngine.review(payload.context)

@app.post("/planning/aace/constructability")
def planning_constructability(payload: PlanningReviewRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    return ConstructabilityEngine.review(payload.context)

@app.post("/planning/xer/validate")
def planning_xer_validate(payload: PlanningXerRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    return XerCreator.validate(payload.model_dump())

@app.post("/planning/xer/create")
def planning_xer_create(payload: PlanningXerRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    try:
        result=XerCreator.save(payload.model_dump(), EXPORT_DIR)
        result['authority']='XER_STAGING_OUTPUT_REQUIRES_NATIVE_P6_IMPORT_AND_CPM_VERIFICATION'
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.get("/planning/xer/download/{filename}")
def planning_xer_download(filename: str, authorization: str | None = Header(default=None)):
    auth(authorization)
    safe=Path(filename).name
    path=EXPORT_DIR/safe
    if path.suffix.lower()!='.xer' or not path.exists(): raise HTTPException(404,'XER not found')
    return FileResponse(path,filename=path.name,media_type='application/octet-stream')

@app.post("/planning/ml/train")
def planning_ml_train(payload: PlanningMLTrainRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    try:
        return PlanningMLHub(ML_DIR/'planning').train(payload.task_name,payload.records,payload.target,
            test_size=payload.test_size,cv_folds=payload.cv_folds,pca_components=payload.pca_components,tune=payload.tune)
    except ValueError as exc: raise HTTPException(status_code=400, detail=str(exc))

@app.post("/planning/ml/predict")
def planning_ml_predict(payload: PlanningMLPredictRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    try: return PlanningMLHub(ML_DIR/'planning').predict(payload.task_name,payload.model_id,payload.records,payload.confidence_threshold)
    except (ValueError,FileNotFoundError) as exc: raise HTTPException(status_code=400, detail=str(exc))

@app.post("/planning/ml/anomaly")
def planning_ml_anomaly(payload: PlanningAnomalyRequest, authorization: str | None = Header(default=None)):
    auth(authorization)
    try: return PlanningMLHub(ML_DIR/'planning').anomaly(payload.records,payload.columns)
    except ValueError as exc: raise HTTPException(status_code=400, detail=str(exc))
