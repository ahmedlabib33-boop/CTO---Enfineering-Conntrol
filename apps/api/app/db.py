from datetime import datetime
from sqlalchemy import create_engine, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from .config import DATABASE_URL

class Base(DeclarativeBase):
    pass

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    original_name: Mapped[str] = mapped_column(String(255))
    stored_path: Mapped[str] = mapped_column(Text)
    sha256: Mapped[str] = mapped_column(String(64), index=True)
    mime_type: Mapped[str] = mapped_column(String(255), default="application/octet-stream")
    kind: Mapped[str] = mapped_column(String(50), default="drawing")
    revision: Mapped[str] = mapped_column(String(100), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class DrawingParse(Base):
    __tablename__ = "drawing_parses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), index=True)
    summary_json: Mapped[str] = mapped_column(Text)
    entities_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class ComparisonRun(Base):
    __tablename__ = "comparison_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    current_document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    reference_document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Change(Base):
    __tablename__ = "changes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comparison_id: Mapped[int] = mapped_column(ForeignKey("comparison_runs.id"), index=True)
    change_key: Mapped[str] = mapped_column(String(80), index=True)
    change_type: Mapped[str] = mapped_column(String(50))
    change_class: Mapped[str] = mapped_column(String(1))
    authority: Mapped[str] = mapped_column(String(80))
    source_handle: Mapped[str] = mapped_column(String(100), default="")
    target_handle: Mapped[str] = mapped_column(String(100), default="")
    before_json: Mapped[str] = mapped_column(Text, default="{}")
    after_json: Mapped[str] = mapped_column(Text, default="{}")
    confidence: Mapped[str] = mapped_column(String(30), default="HIGH")
    status: Mapped[str] = mapped_column(String(30), default="PENDING")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class QaRun(Base):
    __tablename__ = "qa_runs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    file_path: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(30))
    result_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class ExportRecord(Base):
    __tablename__ = "exports"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    export_type: Mapped[str] = mapped_column(String(30))
    file_path: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    action: Mapped[str] = mapped_column(String(100))
    target: Mapped[str] = mapped_column(String(255), default="")
    result: Mapped[str] = mapped_column(String(50), default="OK")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PlanningActivityRecord(Base):
    __tablename__ = "planning_activities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    activity_id: Mapped[str] = mapped_column(String(100), index=True)
    payload_json: Mapped[str] = mapped_column(Text)
    source_lineage_json: Mapped[str] = mapped_column(Text, default="[]")
    review_status: Mapped[str] = mapped_column(String(40), default="REVIEW_REQUIRED")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class PlanningRelationshipRecord(Base):
    __tablename__ = "planning_relationships"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    predecessor: Mapped[str] = mapped_column(String(100), index=True)
    successor: Mapped[str] = mapped_column(String(100), index=True)
    relation_type: Mapped[str] = mapped_column(String(20))
    lag_days: Mapped[str] = mapped_column(String(40), default="0")
    logic_basis: Mapped[str] = mapped_column(Text, default="")
    source_lineage_json: Mapped[str] = mapped_column(Text, default="[]")
    review_status: Mapped[str] = mapped_column(String(40), default="REVIEW_REQUIRED")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class PlanningDecisionRecord(Base):
    __tablename__ = "planning_decisions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    issue_id: Mapped[str] = mapped_column(String(100), index=True)
    decision: Mapped[str] = mapped_column(String(40))
    evidence_json: Mapped[str] = mapped_column(Text, default="[]")
    reason: Mapped[str] = mapped_column(Text, default="")
    reviewer: Mapped[str] = mapped_column(String(120), default="human")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class PlanningModelRegistryRecord(Base):
    __tablename__ = "planning_model_registry"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    task: Mapped[str] = mapped_column(String(100), index=True)
    model_id: Mapped[str] = mapped_column(String(120), index=True)
    status: Mapped[str] = mapped_column(String(40), default="CANDIDATE")
    metadata_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def init_db() -> None:
    Base.metadata.create_all(engine)
