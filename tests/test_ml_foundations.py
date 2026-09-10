from app.services.ml.statistics_engine import StatisticsMathEngine
from app.services.ml.classical_workbench import TabularMLWorkbench
from app.services.ml.unsupervised import UnsupervisedEngineeringML

def _label(move_mm, length_delta, discipline):
    # A real (if simplified) engineering-change severity rule, so the target
    # is an actual function of the features instead of an index coincidence
    # (e.g. `["A","B","C"][i%3]` alongside a feature also keyed by `i%3`) —
    # otherwise a test can pass purely by the pipeline running without
    # ever proving it learned real signal.
    if discipline == "structural" or abs(length_delta) >= 2:
        return "C"
    if move_mm >= 5:
        return "B"
    return "A"

def records(n=60):
    out=[]
    for i in range(n):
        move_mm=float(i%10)
        length_delta=float((i%5)-2)
        discipline=["architecture","mep","structural"][i%3]
        out.append({
            "move_mm":move_mm,
            "length_delta":length_delta,
            "discipline":discipline,
            "confidence":0.5+(i%10)/20,
            "target":_label(move_mm,length_delta,discipline)
        })
    return out

def test_math_stats_bayes():
    assert StatisticsMathEngine.dot([1,2,3],[4,5,6])==32
    assert StatisticsMathEngine.mean([1,2,3,4])==2.5
    assert StatisticsMathEngine.variance([1,2,3,4])==1.25
    assert abs(StatisticsMathEngine.bayes_posterior(0.2,0.8,0.4)-0.4)<1e-12

def test_gradient_descent():
    r=StatisticsMathEngine.gradient_descent_linear_regression([0,1,2,3],[1,3,5,7],0.05,1200)
    assert abs(r["slope"]-2)<0.05 and abs(r["intercept"]-1)<0.05 and r["mse"]<0.01

def test_pipeline_split_metrics_cv_persistence(tmp_path):
    wb=TabularMLWorkbench(tmp_path)
    r=wb.train(records(),target="target",task="classification",model="random_forest",test_size=0.25,cv_folds=5,pca_components=2)
    for k in ["accuracy","precision_weighted","recall_weighted","f1_weighted","confusion_matrix","baseline_accuracy","beats_baseline"]:
        assert k in r["metrics"]
    assert r["cross_validation"]["folds"]>=2
    # The label is a real function of the features (see _label above), so a
    # correctly-trained model must clear the majority-class baseline by a
    # real margin — this is what actually distinguishes "the pipeline runs"
    # from "the pipeline learned something".
    assert r["metrics"]["beats_baseline"] is True
    assert r["metrics"]["accuracy"] > r["metrics"]["baseline_accuracy"] + 0.1
    p=wb.predict(r["model_id"],[{"move_mm":1.0,"length_delta":0.0,"discipline":"mep","confidence":0.9}])
    assert len(p["predictions"])==1

def test_gridsearch(tmp_path):
    wb=TabularMLWorkbench(tmp_path)
    r=wb.train(records(45),target="target",task="classification",model="logistic",cv_folds=3,pca_components=2,tune=True)
    assert r["tuning"] is not None and isinstance(r["best_params"],dict)
    assert r["metrics"]["beats_baseline"] is True

def test_unsupervised():
    rows=[{"x":i,"y":i%4,"text":"x"} for i in range(20)]
    assert len(UnsupervisedEngineeringML.kmeans(rows,3)["labels"])==20
    p=UnsupervisedEngineeringML.pca(rows,2)
    assert len(p["transformed"])==20 and len(p["explained_variance_ratio"])==2
