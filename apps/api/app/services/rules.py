from functools import lru_cache
import yaml
from ..config import RULES_DIR

@lru_cache(maxsize=1)
def load_rules() -> dict:
    with open(RULES_DIR / "default.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def classify(change_type: str) -> tuple[str, str]:
    rules = load_rules().get("classification", {})
    rule = rules.get(change_type, {"class": "C", "authority": "ENGINEERING_APPROVAL_REQUIRED"})
    return str(rule["class"]), str(rule["authority"])
