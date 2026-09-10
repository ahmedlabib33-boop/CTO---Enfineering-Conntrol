\
from __future__ import annotations
import importlib.util

CAPABILITIES = {
    "dataframes": ["pandas"],
    "numerical_linear_algebra": ["numpy", "scipy"],
    "visualization": ["matplotlib", "seaborn"],
    "classical_ml": ["sklearn"],
    "gradient_boosting": ["xgboost", "lightgbm", "catboost"],
    "statistical_modeling": ["statsmodels"],
    "hyperparameter_optimization": ["optuna"],
    "imbalanced_learning": ["imblearn"],
    "model_explainability": ["shap"],
    "manifold_learning": ["umap"],
    "density_clustering": ["hdbscan"],
    "large_tabular_data": ["polars", "dask"],
    "model_exchange": ["onnx", "skl2onnx"],
    "deep_learning": ["torch"],
    "graph_neural_networks": ["torch_geometric"],
    "graph_algorithms": ["networkx"],
    "symbolic_math": ["sympy"],
    "constraint_programming": ["ortools"],
    "smt_constraints": ["z3"],
    "bayesian_inference": ["pymc"],
    "3d_geometry_ml": ["open3d"],
    "computer_vision": ["cv2", "skimage"],
    "local_embeddings": ["sentence_transformers"],
}

def capability_report() -> dict:
    out={}
    for name, modules in CAPABILITIES.items():
        availability={m: bool(importlib.util.find_spec(m)) for m in modules}
        out[name]={"available":all(availability.values()),"modules":availability}
    return out
