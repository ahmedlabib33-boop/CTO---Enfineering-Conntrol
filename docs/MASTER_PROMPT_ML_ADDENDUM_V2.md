# Full ML + Mathematics Foundation

The platform now implements the standard ML foundation as reusable engineering infrastructure.

## Mathematics / statistics
Linear algebra (vectors, matrices, dot products, matrix multiplication), mean, variance, standard deviation, covariance, correlation, distributions, conditional probability, Bayes theorem, calculus/gradient-descent fundamentals, symbolic mathematics, graph mathematics, optimization and constraints.

## Core libraries
NumPy, Pandas, SciPy, Matplotlib, Seaborn, scikit-learn, joblib, SymPy and NetworkX.

Optional capability packs include XGBoost, LightGBM, CatBoost, statsmodels, Optuna, OR-Tools, Z3, imbalanced-learn, SHAP, UMAP, HDBSCAN, Polars, Dask, ONNX, PyTorch, PyTorch Geometric, Open3D, PyMC, JAX/NumPyro, transformers and sentence-transformers.

## Supervised ML
Classification and regression with Random Forest, Logistic Regression and Linear Regression, with extension points for boosted/deep models.

## Unsupervised ML
K-Means and PCA are implemented; UMAP/HDBSCAN are optional capability-pack extensions.

## Correct production workflow
Pandas load/inspect → missing-value handling → numeric/categorical imputation → encoding → scaling → optional PCA → train/test split → `.fit()` → `.predict()` → evaluation → cross-validation → optional GridSearchCV → joblib persistence → deployment → reviewed feedback → retraining.

## Metrics
Classification: accuracy, precision, recall, F1 and confusion matrix.
Regression: MSE, RMSE, MAE and R².

## Engineering governance
Unreviewed model output is never training truth. Project evidence, approved IFC/RFI/specification, deterministic engineering rules and exact constraints remain above ML. A model can recommend but cannot reduce an `ENGINEERING APPROVAL REQUIRED` gate.

## API
- GET `/ml/capabilities`
- POST `/ml/feedback`
- POST `/ml/train`
- GET `/ml/predict-change/{change_id}`
- POST `/ml/workbench/train`
- POST `/ml/workbench/predict/{model_id}`
- POST `/ml/unsupervised`
- POST `/math/statistics`
- POST `/math/symbolic-check`
- GET `/knowledge/search`
