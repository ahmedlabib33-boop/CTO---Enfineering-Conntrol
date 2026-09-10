# ML Learning Governance

Mandatory controls:

- Train only on human-reviewed / authorized examples.
- Keep models project-scoped by default.
- Store model version, feature schema, training count and metrics.
- Never let ML override project document hierarchy.
- Never let ML auto-approve Class C.
- Low confidence or out-of-distribution cases require review.
- Separate training data from source evidence; preserve provenance.
- Do not learn from a model's own unreviewed predictions.
- Compare a new model against the current model before promotion.
- Maintain deterministic fallback when the model is absent, weak or incompatible.
