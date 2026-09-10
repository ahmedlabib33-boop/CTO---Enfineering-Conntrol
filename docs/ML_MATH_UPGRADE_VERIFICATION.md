# ML + Math Upgrade Verification

Verified in the build environment on 10 September 2026:

- Automated tests: **6 passed**.
- Existing DXF parse/compare/modify/QA workflow remains passing.
- Adaptive project-scoped classifier test passes.
- Classifier refuses training when reviewed data is insufficient.
- Reviewed examples can train an online probabilistic classifier.
- Symbolic mathematics test passes.
- Geometry length/area mathematics tests pass.
- Supplied `Construction_Shop_Drawing_Master_Knowledge` was indexed successfully.
- Knowledge index contains **78 persistent chunks** from the supplied knowledge file.
- Knowledge retrieval test passes.
- ML capability registry is exposed through `/ml/capabilities`.
- ML feedback endpoint: `/ml/feedback`.
- ML training endpoint: `/ml/train`.
- ML advisory prediction endpoint: `/ml/predict-change/{change_id}`.
- Exact symbolic-math endpoint: `/math/symbolic-check`.
- Generic engineering knowledge retrieval endpoint: `/knowledge/search`.

## Governance

ML predictions remain advisory. Project authority, hard engineering constraints, deterministic Class A/B/C rules and human approval gates remain higher priority. A deterministic Class C gate cannot be downgraded by the ML classifier.

## Dependency strategy

- `requirements.txt`: application runtime.
- `requirements-ml.txt`: reliable ML/math foundation.
- `requirements-ml-advanced.txt`: boosting, optimization, explainability and advanced statistical engines.
- `requirements-ml-heavy.txt`: deep learning, GNN, Bayesian and 3D/embedding engines.
- `run_app.bat`: installs the core ML pack automatically and attempts advanced/heavy packs while reporting unavailable capabilities instead of simulating them.
