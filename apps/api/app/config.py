from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = ROOT / "data"
UPLOAD_DIR = ROOT / "uploads"
OUTPUT_DIR = ROOT / "outputs"
EXPORT_DIR = ROOT / "exports"
LOG_DIR = ROOT / "logs"
ML_DIR = DATA_DIR / "ml"
KNOWLEDGE_DIR = ROOT / "knowledge"
KNOWLEDGE_INDEX_DIR = DATA_DIR / "knowledge_index"
RULES_DIR = ROOT / "engineering-rules"

for p in (DATA_DIR, UPLOAD_DIR, OUTPUT_DIR, EXPORT_DIR, LOG_DIR, ML_DIR, KNOWLEDGE_INDEX_DIR):
    p.mkdir(parents=True, exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR / 'engineering_cad.db'}")
DEMO_ADMIN_USER = os.getenv("DEMO_ADMIN_USER", "admin")
DEMO_ADMIN_PASSWORD = os.getenv("DEMO_ADMIN_PASSWORD", "admin")
DEMO_TOKEN = os.getenv("DEMO_TOKEN", "dev-admin-token")
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "100"))
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "*").split(",") if o.strip()]
