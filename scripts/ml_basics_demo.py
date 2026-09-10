"""
End-to-end classical ML workflow, applying the standard basis:
linear algebra / stats primitives -> pandas/numpy/sklearn -> supervised
classification -> pipeline-based feature engineering -> evaluation ->
cross-validation -> hyperparameter tuning -> deployment.

Run:
    python scripts/ml_basics_demo.py
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RANDOM_STATE = 42


# ---------------------------------------------------------------------------
# 1. Data handling — load, inspect, simulate real-world missingness
# ---------------------------------------------------------------------------
def load_data() -> tuple[pd.DataFrame, pd.Series]:
    raw = load_breast_cancer(as_frame=True)
    X, y = raw.data, raw.frame["target"]

    print("=== 1. DATA HANDLING ===")
    print(f"shape: {X.shape}")
    print(f"target classes: {dict(y.value_counts())}  (0=malignant, 1=benign)")
    print(f"feature dtypes: {X.dtypes.unique().tolist()}")

    # Real tabular data is rarely complete. Simulate ~4% missing-at-random
    # cells so the imputation step downstream is doing real work.
    rng = np.random.default_rng(RANDOM_STATE)
    mask = rng.random(X.shape) < 0.04
    X = X.mask(mask)
    print(f"missing values injected: {int(X.isna().sum().sum())} cells "
          f"across {int((X.isna().sum() > 0).sum())} columns")
    print()
    return X, y


# ---------------------------------------------------------------------------
# 2. Feature engineering — imputation, scaling, PCA, wrapped in a Pipeline
# ---------------------------------------------------------------------------
def build_pipeline(n_pca_components: int = 10) -> Pipeline:
    # Every step below has to be inside the Pipeline (not applied by hand to
    # the full dataset first) so that fitting only ever sees training folds —
    # this is what keeps cross-validation and grid search honest.
    return Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("pca", PCA(n_components=n_pca_components, random_state=RANDOM_STATE)),
            ("model", RandomForestClassifier(
                n_estimators=300,
                max_depth=None,
                random_state=RANDOM_STATE,
                class_weight="balanced",
            )),
        ]
    )


# ---------------------------------------------------------------------------
# 3/4. Modeling + evaluation — split, fit, predict, metrics, 5-fold CV
# ---------------------------------------------------------------------------
def evaluate(pipeline: Pipeline, X: pd.DataFrame, y: pd.Series) -> Pipeline:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    print("=== 3/4. MODELING + EVALUATION (held-out test set) ===")
    print(f"accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"precision: {precision_score(y_test, y_pred):.4f}")
    print(f"recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"f1:        {f1_score(y_test, y_pred):.4f}")
    print("confusion matrix:")
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred, target_names=["malignant", "benign"]))

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    scores = cross_val_score(pipeline, X, y, cv=cv, scoring="f1_weighted", n_jobs=-1)
    print(f"5-fold CV f1_weighted: mean={scores.mean():.4f}  std={scores.std():.4f}  "
          f"folds={np.round(scores, 4).tolist()}")
    print()
    return pipeline


# ---------------------------------------------------------------------------
# 5. Hyperparameter tuning — GridSearchCV over PCA components + forest shape
# ---------------------------------------------------------------------------
def tune(pipeline: Pipeline, X: pd.DataFrame, y: pd.Series) -> Pipeline:
    param_grid = {
        "pca__n_components": [5, 10, 15],
        "model__n_estimators": [200, 300, 500],
        "model__max_depth": [None, 8, 16],
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    search = GridSearchCV(
        pipeline, param_grid, cv=cv, scoring="f1_weighted", n_jobs=-1, refit=True
    )
    search.fit(X, y)

    print("=== 5. HYPERPARAMETER TUNING (GridSearchCV) ===")
    print(f"best params: {search.best_params_}")
    print(f"best CV f1_weighted: {search.best_score_:.4f}")
    print()
    return search.best_estimator_


# ---------------------------------------------------------------------------
# 6. Deployment note — persist the *whole* fitted pipeline, not just the model
# ---------------------------------------------------------------------------
def deployment_note() -> None:
    print("=== 6. DEPLOYMENT (commented pattern — see code) ===")
    print("import joblib")
    print('joblib.dump(best_pipeline, "model.joblib")   # save preprocessing + model together')
    print('loaded = joblib.load("model.joblib")          # later, in production')
    print("loaded.predict(new_raw_records)                # imputer/scaler/PCA reapplied automatically")
    # Left as a comment/pattern rather than a real write: this script's job is
    # to demonstrate the workflow, not to leave a stray artifact on disk.
    # best_pipeline is already the correct object to persist — see tune().


def main() -> None:
    X, y = load_data()
    baseline = build_pipeline()
    evaluate(baseline, X, y)
    best_pipeline = tune(build_pipeline(), X, y)
    evaluate(best_pipeline, X, y)
    deployment_note()


if __name__ == "__main__":
    main()
