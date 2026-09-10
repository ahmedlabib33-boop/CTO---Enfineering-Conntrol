# ML / Math / Engineering Library Matrix

| Capability | Primary libraries | Engineering use |
|---|---|---|
| Numerical arrays / linear algebra | NumPy, SciPy | vectors, matrices, tolerances, transformations, optimization |
| Symbolic mathematics | SymPy | formula checking, simplification, exact relationships |
| Classical ML | scikit-learn | classification, regression, anomaly/OOD, clustering, calibration |
| Gradient boosting | XGBoost, LightGBM, CatBoost | structured engineering/change-risk models |
| Deep learning | PyTorch | vision, embeddings, sequence/geometry models |
| Graph neural networks | PyTorch Geometric | semantic drawing graph, object/interface reasoning |
| Graph algorithms | NetworkX | connectivity, impact propagation, paths, topology |
| Constraint optimization | OR-Tools | layout, assignment, sequencing, routing, discrete optimization |
| SMT constraint solving | Z3 | hard logical/numeric engineering constraint satisfiability |
| Bayesian inference | PyMC, ArviZ | uncertainty, posterior risk, probabilistic engineering models |
| Hyperparameter optimization | Optuna | model tuning under controlled evaluation |
| Explainability | SHAP | feature-attribution for reviewed model outputs |
| Statistics | statsmodels | regression, diagnostics, statistical tests |
| Imbalanced learning | imbalanced-learn | rare Class C / defect / anomaly handling |
| 2D CAD / geometry | ezdxf, Shapely, GEOS, Rtree | CAD parsing, topology, spatial matching |
| BIM semantics | IfcOpenShell | IFC object/property/relationship extraction |
| Computer vision | OpenCV, scikit-image | raster drawing preprocessing and geometry recovery |
| 3D geometry | Open3D | point clouds, meshes, registration, 3D ML |
| Local semantic embeddings | sentence-transformers, Transformers | evidence retrieval and semantic similarity |

The platform should not import every library into every request. A capability registry selects the lightest valid engine for the task and reports unavailable optional capabilities instead of simulating success.
