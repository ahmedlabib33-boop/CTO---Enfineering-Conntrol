\
from app.services.ml.features import change_features
from app.services.ml.adaptive import AdaptiveChangeClassifier
from app.services.ml.math_engine import EngineeringMathEngine


def sample_change(i=0):
    return {
        "change_type":"MOVED" if i%2==0 else "TEXT_CHANGED",
        "before":{"type":"LINE","layer":"A","centroid":[0,0,0],"length":10.0,"text":"A"},
        "after":{"type":"LINE","layer":"A","centroid":[i+1,0,0],"length":10.0,"text":"B" if i%2 else "A"},
    }


def test_math_geometry_and_symbolic():
    assert EngineeringMathEngine.polyline_length([[0,0],[3,4]]) == 5.0
    assert EngineeringMathEngine.polygon_area([[0,0],[4,0],[4,3],[0,3]]) == 12.0
    r=EngineeringMathEngine.symbolic_check("x**2 + 2*x + 1", {"x":2})
    assert r["value"] == "9"


def test_adaptive_learning_requires_reviewed_examples(tmp_path):
    model=AdaptiveChangeClassifier(tmp_path, project_id=1)
    r=model.train(minimum_examples=4)
    assert r["status"] == "INSUFFICIENT_REVIEWED_DATA"
    for i,label in enumerate(["A","B","A","B","A","B"]):
        model.record_reviewed_example(sample_change(i), label, "tester")
    r=model.train(minimum_examples=4)
    assert r["status"] == "TRAINED"
    p=model.predict(sample_change(8), min_confidence=0.0)
    assert p["suggested_class"] in {"A","B","C"}


def _labeled_change(i, cls):
    """Synthetic-but-learnable reviewed changes: a small in-place edit (A),
    a text-only edit (B), or a large relocation (C) — so a trained
    classifier has a real signal to separate, instead of an arbitrary
    alternating label with no feature basis."""
    if cls == "A":
        return {"change_type":"MOVED",
                "before":{"type":"LINE","layer":"A","centroid":[0,0,0],"length":10.0,"text":"A"},
                "after":{"type":"LINE","layer":"A","centroid":[0.1+(i%3)*0.05,0,0],"length":10.0,"text":"A"}}
    if cls == "B":
        return {"change_type":"TEXT_CHANGED",
                "before":{"type":"TEXT","layer":"A","centroid":[0,0,0],"length":0.0,"text":"A"},
                "after":{"type":"TEXT","layer":"A","centroid":[0,0,0],"length":0.0,"text":f"B{i%3}"}}
    return {"change_type":"MOVED",
            "before":{"type":"LINE","layer":"A","centroid":[0,0,0],"length":10.0,"text":"A"},
            "after":{"type":"LINE","layer":"A","centroid":[40+(i%5)*2,0,0],"length":10.0,"text":"A"}}


def test_adaptive_reports_honest_cv_and_beats_baseline(tmp_path):
    model=AdaptiveChangeClassifier(tmp_path, project_id=7)
    i=0
    for cls in ("A","B","C"):
        for _ in range(6):
            model.record_reviewed_example(_labeled_change(i, cls), cls, "tester")
            i+=1
    r=model.train(minimum_examples=15)
    assert r["status"]=="TRAINED"
    assert r["model_version"]==1
    # Cross-validated on held-out folds, not resubstitution on the training
    # rows themselves — the honest generalization estimate.
    assert r["cross_validation"]["status"]=="COMPUTED"
    assert r["cross_validation"]["accuracy_mean"]>0.6
    assert r["beats_baseline"] is True
    assert r["baseline_comparison_basis"]=="cross_validation"

    # Retraining on more reviewed examples must version forward and append
    # to the provenance log, not silently overwrite it.
    for _ in range(3):
        model.record_reviewed_example(_labeled_change(i,"A"),"A","tester"); i+=1
    r2=model.train(minimum_examples=15)
    assert r2["model_version"]==2
    history=model.training_history()
    assert len(history)==2
    assert [h["model_version"] for h in history]==[1,2]


def test_adaptive_class_diversity_guard(tmp_path):
    model=AdaptiveChangeClassifier(tmp_path, project_id=8)
    for i in range(20):
        model.record_reviewed_example(_labeled_change(i,"A"),"A","tester")
    r=model.train(minimum_examples=10)
    assert r["status"]=="INSUFFICIENT_CLASS_DIVERSITY"


def test_adaptive_persists_across_instances(tmp_path):
    model=AdaptiveChangeClassifier(tmp_path, project_id=9)
    i=0
    for cls in ("A","B","C"):
        for _ in range(6):
            model.record_reviewed_example(_labeled_change(i,cls), cls, "tester"); i+=1
    r=model.train(minimum_examples=15)

    reloaded=AdaptiveChangeClassifier(tmp_path, project_id=9)
    assert reloaded.fitted is True
    assert reloaded.model_version==r["model_version"]
    p=reloaded.predict(_labeled_change(999,"C"), min_confidence=0.0)
    assert p["suggested_class"] in {"A","B","C"}
    assert p["model_version"]==r["model_version"]
