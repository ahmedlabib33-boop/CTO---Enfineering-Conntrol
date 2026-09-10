from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str
    password: str

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)

class ComparisonCreate(BaseModel):
    project_id: int
    current_document_id: int
    reference_document_id: int

class ModificationCreate(BaseModel):
    comparison_id: int

class QaCreate(BaseModel):
    project_id: int
    file_path: str

class ExportCreate(BaseModel):
    project_id: int
    comparison_id: int
    revised_dxf_path: str

class MlFeedback(BaseModel):
    project_id: int
    change_id: int
    reviewed_class: str
    reviewer: str = "human"

class MlTrainRequest(BaseModel):
    project_id: int
    minimum_examples: int = 12

class MathSymbolicRequest(BaseModel):
    expression: str
    substitutions: dict[str, float] = {}


class MlWorkbenchTrainRequest(BaseModel):
    records: list[dict]
    target: str
    task: str = "classification"
    model: str = "random_forest"
    test_size: float = 0.2
    cv_folds: int = 5
    pca_components: int | None = None
    tune: bool = False

class MlWorkbenchPredictRequest(BaseModel):
    records: list[dict]

class MlUnsupervisedRequest(BaseModel):
    records: list[dict]
    method: str = "pca"
    columns: list[str] | None = None
    components: int = 2
    clusters: int = 3

class MathStatsRequest(BaseModel):
    operation: str
    values: list[float] = []
    values_b: list[float] = []
    prior: float | None = None
    likelihood: float | None = None
    evidence: float | None = None
    joint_count: float | None = None
    condition_count: float | None = None


class PlanningDurationRequest(BaseModel):
    quantity: float | None = None
    rate: float | None = None
    rate_basis: str = 'UNKNOWN'
    crews: float | None = None
    shift_hours: float | None = None
    productive_hours: float | None = None
    labor_per_crew: float | None = None
    equipment_units_per_crew: float | None = None
    operating_hours: float | None = None
    time_based_duration: float | None = None
    round_up: bool = True
    source_ids: list[str] = []

class PlanningProcurementRequest(BaseModel):
    required_on_site_date: str
    lead_time_days: float
    planned_procurement_start: str | None = None
    source_verified: bool = True
    tight_buffer_days: int | None = None

class PlanningScheduleQARequest(BaseModel):
    activities: list[dict]
    relationships: list[dict] = []
    excessive_lag_days: float | None = None

class PlanningReviewRequest(BaseModel):
    context: dict = {}

class PlanningXerRequest(BaseModel):
    project_name: str
    project_code: str
    planned_start: str
    data_date: str | None = None
    hours_per_day: float
    workdays_per_week: float
    calendar_name: str = ''
    activities: list[dict]
    relationships: list[dict] = []
    schedule_context: dict = {}

class PlanningMLTrainRequest(BaseModel):
    task_name: str
    records: list[dict]
    target: str
    test_size: float = 0.2
    cv_folds: int = 5
    pca_components: int | None = None
    tune: bool = False

class PlanningMLPredictRequest(BaseModel):
    task_name: str
    model_id: str
    records: list[dict]
    confidence_threshold: float = 0.70

class PlanningAnomalyRequest(BaseModel):
    records: list[dict]
    columns: list[str] | None = None
