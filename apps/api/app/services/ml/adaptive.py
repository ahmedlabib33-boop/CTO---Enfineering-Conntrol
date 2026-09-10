\
from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import json
import math
import joblib
import numpy as np
from sklearn.feature_extraction import FeatureHasher
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, f1_score, log_loss
from sklearn.model_selection import StratifiedKFold
from .features import change_features

CLASSES = np.array(["A", "B", "C"])

class AdaptiveChangeClassifier:
    """
    Project-scoped classifier, retrained from scratch on the full reviewed-example
    log each time train() is called.

    It never overrides engineering authority. It predicts a proposed class and
    confidence; deterministic/project rules and human approval remain the gate.

    Evaluation is honest by construction: every train() call reports both a
    resubstitution figure (fit on everything, for reference only) and a
    stratified cross-validated estimate computed on held-out folds, plus a
    majority-class baseline so "the model beats guessing" is never assumed.
    """
    def __init__(self, model_dir: str | Path, project_id: int, n_features: int = 2048):
        self.project_id = int(project_id)
        self.root = Path(model_dir) / f"project_{self.project_id}"
        self.root.mkdir(parents=True, exist_ok=True)
        self.examples_path = self.root / "approved_examples.jsonl"
        self.model_path = self.root / "change_classifier.joblib"
        self.meta_path = self.root / "model_meta.json"
        self.history_path = self.root / "training_history.jsonl"

        self.n_features = n_features
        self.model_version = 0
        self.hasher = FeatureHasher(n_features=n_features, input_type="dict", alternate_sign=False)
        self.model = SGDClassifier(loss="log_loss", penalty="elasticnet", alpha=0.0005, random_state=42)
        self.fitted = False
        if self.model_path.exists():
            bundle = joblib.load(self.model_path)
            self.model = bundle["model"]
            self.hasher = bundle["hasher"]
            # Persisted hasher dimensionality is authoritative once a model
            # exists, so later retrains stay compatible with it even if a
            # caller constructs this class with a different n_features.
            self.n_features = getattr(self.hasher, "n_features", n_features)
            self.model_version = int(bundle.get("model_version", 0))
            self.fitted = True

    @staticmethod
    def _encode_row(row: dict) -> dict:
        encoded: dict[str, float] = {}
        for k, v in row.items():
            if isinstance(v, str):
                encoded[f"{k}={v}"] = 1.0
            else:
                try: encoded[k] = float(v)
                except Exception: pass
        return encoded

    def _vectorize(self, rows: list[dict]):
        return self.hasher.transform([self._encode_row(r) for r in rows])

    def record_reviewed_example(self, change: dict, reviewed_class: str, reviewer: str = "human") -> dict:
        reviewed_class = reviewed_class.upper().strip()
        if reviewed_class not in set(CLASSES):
            raise ValueError("reviewed_class must be A, B, or C")
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "project_id": self.project_id,
            "reviewer": reviewer,
            "label": reviewed_class,
            "features": change_features(change),
        }
        with self.examples_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        return record

    def load_examples(self) -> list[dict]:
        if not self.examples_path.exists(): return []
        out=[]
        for line in self.examples_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try: out.append(json.loads(line))
                except json.JSONDecodeError: pass
        return out

    def training_history(self) -> list[dict]:
        if not self.history_path.exists(): return []
        out=[]
        for line in self.history_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                try: out.append(json.loads(line))
                except json.JSONDecodeError: pass
        return out

    def _fresh_model(self) -> SGDClassifier:
        return SGDClassifier(loss="log_loss", penalty="elasticnet", alpha=0.0005, random_state=42)

    def _cross_validate(self, X, y: np.ndarray) -> dict:
        """Stratified k-fold CV with a fresh model per fold — the only honest
        way to estimate generalization from a small, growing reviewed-example
        log. Returns a status dict explaining why CV was skipped when the
        per-class example count is too small to stratify at all."""
        counts = Counter(y.tolist())
        min_class_count = min(counts.values())
        if min_class_count < 2:
            return {"status": "INSUFFICIENT_PER_CLASS_EXAMPLES_FOR_CV", "min_class_count": int(min_class_count)}

        folds = max(2, min(5, min_class_count))
        skf = StratifiedKFold(n_splits=folds, shuffle=True, random_state=42)
        accs, f1s = [], []
        for train_idx, test_idx in skf.split(X, y):
            fold_model = self._fresh_model()
            fold_model.partial_fit(X[train_idx], y[train_idx], classes=CLASSES)
            pred = fold_model.predict(X[test_idx])
            accs.append(float(accuracy_score(y[test_idx], pred)))
            f1s.append(float(f1_score(y[test_idx], pred, average="macro", zero_division=0)))
        return {
            "status": "COMPUTED",
            "folds": int(folds),
            "accuracy_mean": float(np.mean(accs)),
            "accuracy_std": float(np.std(accs)),
            "f1_macro_mean": float(np.mean(f1s)),
            "f1_macro_std": float(np.std(f1s)),
            "scores": accs,
        }

    def train(self, minimum_examples: int = 12) -> dict:
        examples = self.load_examples()
        if len(examples) < minimum_examples:
            return {"status":"INSUFFICIENT_REVIEWED_DATA","reviewed_examples":len(examples),"minimum":minimum_examples}

        y = np.array([e["label"] for e in examples])
        if len(set(y.tolist())) < 2:
            return {"status":"INSUFFICIENT_CLASS_DIVERSITY","classes":sorted(set(y.tolist()))}

        # A fresh hasher + fresh model every retrain, fit once on the complete
        # reviewed-example log. Reusing the persisted (already-fitted) model
        # across retrains would repeatedly re-expose it to the same growing
        # history via partial_fit, over-weighting older examples with every
        # call — this keeps training reproducible purely from the jsonl log.
        hasher = FeatureHasher(n_features=self.n_features, input_type="dict", alternate_sign=False)
        X = hasher.transform([self._encode_row(e["features"]) for e in examples])

        majority_label, majority_count = Counter(y.tolist()).most_common(1)[0]
        baseline_accuracy = majority_count / len(y)

        cross_validation = self._cross_validate(X, y)

        model = self._fresh_model()
        model.partial_fit(X, y, classes=CLASSES)
        pred = model.predict(X)
        proba = model.predict_proba(X)
        metrics = {"training_accuracy": float(accuracy_score(y, pred))}
        try: metrics["training_log_loss"] = float(log_loss(y, proba, labels=CLASSES))
        except Exception: pass

        if cross_validation.get("status") == "COMPUTED":
            beats_baseline = cross_validation["accuracy_mean"] > baseline_accuracy
            baseline_comparison_basis = "cross_validation"
        else:
            beats_baseline = metrics["training_accuracy"] > baseline_accuracy
            baseline_comparison_basis = "resubstitution"

        self.model = model
        self.hasher = hasher
        self.fitted = True
        self.model_version += 1
        joblib.dump({"model": self.model, "hasher": self.hasher, "model_version": self.model_version}, self.model_path)

        meta={
            "status":"TRAINED",
            "project_id":self.project_id,
            "model_version":self.model_version,
            "reviewed_examples":len(examples),
            "classes":sorted(set(y.tolist())),
            **metrics,
            "cross_validation":cross_validation,
            "baseline_accuracy":float(baseline_accuracy),
            "baseline_majority_class":str(majority_label),
            "beats_baseline":bool(beats_baseline),
            "baseline_comparison_basis":baseline_comparison_basis,
        }
        self.meta_path.write_text(json.dumps(meta,indent=2),encoding="utf-8")
        with self.history_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"timestamp": datetime.now(timezone.utc).isoformat(), **meta}, ensure_ascii=False) + "\n")
        return meta

    def predict(self, change: dict, min_confidence: float = 0.70) -> dict:
        if not self.fitted:
            return {"status":"MODEL_NOT_TRAINED","suggested_class":None,"confidence":0.0,"authority":"DETERMINISTIC_RULES_ONLY"}
        X = self._vectorize([change_features(change)])
        p = self.model.predict_proba(X)[0]
        idx = int(np.argmax(p))
        label = str(self.model.classes_[idx])
        confidence = float(p[idx])
        probs = {str(c):float(v) for c,v in zip(self.model.classes_,p)}
        if confidence < min_confidence:
            return {"status":"LOW_CONFIDENCE","suggested_class":label,"confidence":confidence,"probabilities":probs,"authority":"HUMAN_REVIEW_REQUIRED","model_version":self.model_version}
        return {"status":"PREDICTED","suggested_class":label,"confidence":confidence,"probabilities":probs,"authority":"ADVISORY_ONLY","model_version":self.model_version}
