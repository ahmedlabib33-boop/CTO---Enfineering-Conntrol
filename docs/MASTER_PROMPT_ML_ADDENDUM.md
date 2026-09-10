# 74. MACHINE-LEARNING, MATHEMATICAL AND ADAPTIVE ENGINEERING INTELLIGENCE

The platform shall include an ML and mathematical intelligence layer that learns from reviewed project outcomes while preserving project authority and engineering approval boundaries.

It must support, where applicable: supervised learning, online/incremental learning, gradient boosting, anomaly detection, clustering, similarity learning, computer vision, graph learning, Bayesian uncertainty, explainability, optimization, symbolic mathematics, graph algorithms, constraint programming and SAT/SMT constraint validation.

The coding agent shall implement a capability registry and use the best available valid engine for each problem rather than force every problem through one model.

### Learning sources

Permitted training labels include reviewed: entity matches, Class A/B/C decisions, approvals/rejections/holds, corrected metadata, resolved conflicts, accepted object tags, QA findings, quantity corrections and engineering-rule outcomes.

Unreviewed AI predictions MUST NOT become training truth.

### Hybrid decision priority

```text
PROJECT AUTHORITY / APPROVED EVIDENCE
        ↓
HARD ENGINEERING / SAFETY CONSTRAINTS
        ↓
EXACT MATHEMATICS / GEOMETRY / SOLVERS
        ↓
DETERMINISTIC ENGINEERING RULES
        ↓
ML PREDICTION / RANKING / RECOGNITION
        ↓
CONFIDENCE + OOD GATE
        ↓
HUMAN ENGINEERING REVIEW
        ↓
AUTHORIZED OUTCOME
        ↓
REVIEWED TRAINING EXAMPLE
```

ML must never downgrade an approval requirement imposed by higher layers.

### Required model families

The architecture must permit: linear/logistic models, SVM, nearest-neighbor methods, random forests, extremely randomized trees, gradient boosting, XGBoost, LightGBM, CatBoost, neural networks, CNN/vision models, graph neural networks, clustering, dimensionality reduction, isolation/novelty detection, Bayesian models and calibrated ensembles.

### Required mathematics

Support the mathematical tools needed for engineering inference: linear algebra, vector geometry, analytic geometry, transformations, numerical methods, interpolation, regression, robust statistics, probability, Bayesian inference, graph theory, computational geometry, symbolic algebra, optimization, constraint programming, SAT/SMT, similarity metrics, topology and uncertainty calculations.

### Library policy

Use capability-oriented dependency packs. `requirements.txt` contains the reliable runtime core. `requirements-ml.txt` contains the mandatory ML/math pack. `requirements-ml-heavy.txt` contains heavy/hardware-sensitive optional engines. `run_app.bat` installs the core and ML packs automatically and attempts heavy capabilities without making the entire application fake or unusable when a platform-specific wheel is unavailable.

### ML endpoints

The implementation shall expose at minimum:

```text
GET  /ml/capabilities
POST /ml/feedback
POST /ml/train
GET  /ml/predict-change/{change_id}
```

The system must preserve the deterministic class/authority result beside the ML recommendation.
