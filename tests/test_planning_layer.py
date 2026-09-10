from pathlib import Path
from app.services.planning import DurationEngine, ProcurementEngine, ScheduleQAEngine, ScheduleBasisEngine, XerCreator, PlanningMLHub

def test_duration_exact_example():
    r=DurationEngine.calculate(quantity=2400,rate=300,rate_basis='CREW_DAILY_PRODUCTION',crews=2)
    assert r['status']=='CALCULATED' and r['raw_duration_days']==4.0 and r['planned_duration_days']==4

def test_duration_refuses_missing_crew():
    r=DurationEngine.calculate(quantity=2400,rate=300,rate_basis='CREW_DAILY_PRODUCTION')
    assert r['status']=='MISSING' and 'crews' in r['missing']

def test_procurement_backward_need_date():
    r=ProcurementEngine.analyze('2026-12-31',45,'2026-11-01',True)
    assert r['latest_safe_procurement_start']=='2026-11-16' and r['status']=='PROCUREMENT_OK'

def test_schedule_qa_flags_missing_and_open_ends():
    acts=[{'activity_id':'A1','activity_name':'Start','activity_type':'START_MILESTONE','duration_days':0,'calendar':'C1'},
          {'activity_id':'A2','activity_name':'Work','duration_days':5,'calendar':'C1'},
          {'activity_id':'A3','activity_name':'Finish','activity_type':'FINISH_MILESTONE','duration_days':0,'calendar':'C1'}]
    qa=ScheduleQAEngine.review(acts,[{'predecessor':'A1','successor':'A2','type':'FS'}])
    assert any(x['code']=='OPEN_FINISH' and x['activity_id']=='A2' for x in qa['issues'])

def test_aace_guidance_does_not_fake_complete():
    r=ScheduleBasisEngine.review({'scope':'Defined'})
    assert r['basis']=='GUIDANCE_NOT_CONTRACT_STANDARD' and r['status']=='REVIEW_REQUIRED' and r['coverage_percent']<100

def test_xer_staging_structure(tmp_path):
    p={'project_name':'Demo','project_code':'DEMO','planned_start':'2026-09-10','data_date':'2026-09-10','hours_per_day':8,'workdays_per_week':6,'calendar_name':'8h x 6d','activities':[
       {'activity_id':'M001','activity_name':'Start','activity_type':'START_MILESTONE','duration_days':0,'wbs_code':'01'},
       {'activity_id':'A001','activity_name':'Excavation','duration_days':5,'wbs_code':'07'},
       {'activity_id':'M999','activity_name':'Finish','activity_type':'FINISH_MILESTONE','duration_days':0,'wbs_code':'24'}],
       'relationships':[{'predecessor':'M001','successor':'A001','type':'FS','lag_days':0},{'predecessor':'A001','successor':'M999','type':'FS','lag_days':0}]}
    v=XerCreator.validate(p); assert v['valid'] and v['p6_native_verification_required']
    text=XerCreator.build(p)
    for section in ['%T\tCALENDAR','%T\tPROJECT','%T\tPROJWBS','%T\tTASK','%T\tTASKPRED','%E']:
        assert section in text
    saved=XerCreator.save(p,tmp_path); assert Path(saved['path']).exists()

def _procurement_label(lead_time, days_to_need, engineering_ready, supplier_score):
    # A real procurement-risk rule (short slack, or not engineering-ready
    # with a weak supplier) instead of `'LATE' if i%3==0 else ...` — that
    # older rule keyed off `i%3` while every feature below cycles on
    # periods coprime with 3 (5, 7, 2, 10), so the label carried zero
    # relationship to the features it was supposedly a function of and no
    # model could ever learn it above the majority-class baseline.
    if (days_to_need - lead_time) < -10:
        return 'LATE'
    if engineering_ready == 0 and supplier_score < 0.8:
        return 'LATE'
    return 'ON_TIME'

def _ml_records(n=45):
    out=[]
    for i in range(n):
        lead_time=30+(i%5)*5
        days_to_need=20+(i%7)*6
        engineering_ready=i%2
        supplier_score=0.5+(i%10)/20
        label=_procurement_label(lead_time,days_to_need,engineering_ready,supplier_score)
        out.append({'lead_time':lead_time,'days_to_need':days_to_need,'engineering_ready':engineering_ready,'supplier_score':supplier_score,'label':label})
    return out

def test_planning_ml_hub_train_predict_and_governance(tmp_path):
    hub=PlanningMLHub(tmp_path)
    r=hub.train('procurement_risk',_ml_records(),target='label',cv_folds=3)
    assert r['governance']=='ADVISORY_ONLY_HUMAN_REVIEW'
    # Same principle as the classical-workbench test: the label is now a
    # real function of the features, so the trained model must actually
    # beat guessing the majority class, not merely finish without error.
    assert r['metrics']['beats_baseline'] is True
    p=hub.predict('procurement_risk',r['model_id'],[{'lead_time':50,'days_to_need':20,'engineering_ready':0,'supplier_score':0.6}],confidence_threshold=0.99)
    assert p['authority']=='ML_RECOMMENDATION_ONLY' and p['confidence_gate'][0]['status'] in {'RECOMMEND','ABSTAIN_REVIEW_REQUIRED'}

def test_anomaly_is_review_not_error(tmp_path):
    hub=PlanningMLHub(tmp_path)
    r=hub.anomaly([{'duration':5,'lag':0},{'duration':6,'lag':0},{'duration':5.5,'lag':0},{'duration':90,'lag':45},{'duration':6,'lag':0}])
    assert r['status']=='COMPLETED' and r['governance']=='ANOMALY_MEANS_REVIEW_REQUIRED_NOT_ERROR'
