from __future__ import annotations
from pathlib import Path
from uuid import uuid4
import json, joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

class TabularMLWorkbench:
    """Pandas -> preprocessing -> split -> fit -> evaluate -> CV -> tune -> persist."""
    def __init__(self, model_dir: str | Path):
        self.model_dir=Path(model_dir); self.model_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _frame(records):
        if not records: raise ValueError("records cannot be empty")
        return pd.DataFrame.from_records(records)

    @staticmethod
    def _columns(X):
        numeric=X.select_dtypes(include=[np.number,"bool"]).columns.tolist()
        categorical=[c for c in X.columns if c not in numeric]
        return numeric,categorical

    @staticmethod
    def _estimator(task, model, random_state):
        task,model=task.lower(),model.lower()
        if task=="classification":
            if model in {"random_forest","randomforest","rf"}:
                return RandomForestClassifier(n_estimators=200,random_state=random_state,class_weight="balanced")
            if model in {"logistic","logistic_regression"}:
                return LogisticRegression(max_iter=3000,class_weight="balanced")
        if task=="regression":
            if model in {"random_forest","randomforest","rf"}:
                return RandomForestRegressor(n_estimators=200,random_state=random_state)
            if model in {"linear","linear_regression"}:
                return LinearRegression()
        raise ValueError(f"Unsupported task/model: {task}/{model}")

    @staticmethod
    def _pipeline(X, estimator, pca_components=None):
        numeric,categorical=TabularMLWorkbench._columns(X)
        num_steps=[("imputer",SimpleImputer(strategy="median")),("scaler",StandardScaler())]
        if pca_components is not None and numeric:
            num_steps.append(("pca",PCA(n_components=max(1,min(int(pca_components),len(numeric))))))
        transformers=[]
        if numeric: transformers.append(("num",Pipeline(num_steps),numeric))
        if categorical:
            transformers.append(("cat",Pipeline([
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("onehot",OneHotEncoder(handle_unknown="ignore",sparse_output=False)),
            ]),categorical))
        if not transformers: raise ValueError("No usable feature columns")
        return Pipeline([("preprocess",ColumnTransformer(transformers)),("model",estimator)]),numeric,categorical

    def train(self, records, target, task="classification", model="random_forest", test_size=0.2, cv_folds=5, pca_components=None, tune=False, random_state=42):
        df=self._frame(records)
        if target not in df.columns: raise ValueError(f"target column '{target}' not found")
        df=df.dropna(subset=[target]).copy()
        if len(df)<6: raise ValueError("At least 6 labeled records are required")
        X,y=df.drop(columns=[target]),df[target]
        pipe,numeric,categorical=self._pipeline(X,self._estimator(task,model,random_state),pca_components)
        stratify=y if task=="classification" and y.nunique()>1 and y.value_counts().min()>=2 else None
        Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=test_size,random_state=random_state,stratify=stratify)

        tuning=None; best_params={}
        if tune:
            if model.lower() in {"random_forest","randomforest","rf"}:
                grid={"model__n_estimators":[100,200,400],"model__max_depth":[None,8,16],"model__min_samples_leaf":[1,2,4]}
            elif task=="classification":
                grid={"model__C":[0.1,1.0,10.0]}
            else:
                grid={}
            if pca_components is not None and numeric:
                max_pc=max(1,min(len(numeric),len(Xtr)-1))
                grid["preprocess__num__pca__n_components"]=sorted(set([1,min(2,max_pc),max_pc]))
            if grid:
                scoring="f1_weighted" if task=="classification" else "neg_root_mean_squared_error"
                folds=max(2,min(int(cv_folds),len(Xtr)))
                if task=="classification":
                    folds=min(folds,int(ytr.value_counts().min()))
                search=GridSearchCV(pipe,grid,cv=max(2,folds),scoring=scoring,n_jobs=-1,refit=True)
                search.fit(Xtr,ytr); pipe=search.best_estimator_
                best_params=search.best_params_
                tuning={"best_score":float(search.best_score_),"best_params":best_params}
            else: pipe.fit(Xtr,ytr)
        else: pipe.fit(Xtr,ytr)

        pred=pipe.predict(Xte)
        # A trivial baseline fit on the same split, so a reported accuracy/RMSE
        # is never read in isolation without knowing whether the model beat
        # guessing the majority class / the training-set mean.
        if task=="classification":
            dummy=DummyClassifier(strategy="most_frequent",random_state=random_state).fit(Xtr,ytr)
            baseline_pred=dummy.predict(Xte)
            metrics={
                "accuracy":float(accuracy_score(yte,pred)),
                "precision_weighted":float(precision_score(yte,pred,average="weighted",zero_division=0)),
                "recall_weighted":float(recall_score(yte,pred,average="weighted",zero_division=0)),
                "f1_weighted":float(f1_score(yte,pred,average="weighted",zero_division=0)),
                "confusion_matrix":confusion_matrix(yte,pred).tolist(),
                "baseline_accuracy":float(accuracy_score(yte,baseline_pred)),
                "baseline_strategy":"most_frequent_class",
            }
            metrics["beats_baseline"]=metrics["accuracy"]>metrics["baseline_accuracy"]
        else:
            mse=float(mean_squared_error(yte,pred))
            dummy=DummyRegressor(strategy="mean").fit(Xtr,ytr)
            baseline_pred=dummy.predict(Xte)
            baseline_rmse=float(np.sqrt(mean_squared_error(yte,baseline_pred)))
            metrics={"mse":mse,"rmse":float(np.sqrt(mse)),"mae":float(mean_absolute_error(yte,pred)),"r2":float(r2_score(yte,pred)),
                     "baseline_rmse":baseline_rmse,"baseline_strategy":"mean_target"}
            metrics["beats_baseline"]=metrics["rmse"]<baseline_rmse

        folds=max(2,min(int(cv_folds),len(df)))
        if task=="classification": folds=min(folds,int(y.value_counts().min()))
        cv=None
        if folds>=2:
            scoring="f1_weighted" if task=="classification" else "neg_root_mean_squared_error"
            scores=cross_val_score(pipe,X,y,cv=folds,scoring=scoring,n_jobs=-1)
            cv={"folds":int(folds),"scoring":scoring,"scores":[float(v) for v in scores],"mean":float(np.mean(scores)),"std":float(np.std(scores))}

        model_id=uuid4().hex
        path=self.model_dir/f"{model_id}.joblib"
        bundle={"pipeline":pipe,"target":target,"task":task,"model_name":model,"feature_columns":X.columns.tolist(),"numeric_columns":numeric,"categorical_columns":categorical}
        joblib.dump(bundle,path)
        meta={"model_id":model_id,"task":task,"model":model,"target":target,"rows":int(len(df)),"features":X.columns.tolist(),"metrics":metrics,"cross_validation":cv,"tuning":tuning,"best_params":best_params,"model_path":str(path)}
        (self.model_dir/f"{model_id}.json").write_text(json.dumps(meta,indent=2,default=str),encoding="utf-8")
        return meta

    def predict(self, model_id, records):
        path=self.model_dir/f"{model_id}.joblib"
        if not path.exists(): raise FileNotFoundError(model_id)
        bundle=joblib.load(path); df=self._frame(records)
        for c in bundle["feature_columns"]:
            if c not in df.columns: df[c]=np.nan
        X=df[bundle["feature_columns"]]; pipe=bundle["pipeline"]; pred=pipe.predict(X)
        out={"model_id":model_id,"predictions":[x.item() if hasattr(x,"item") else x for x in pred]}
        try:
            probs=pipe.predict_proba(X); classes=[str(c) for c in pipe.classes_]
            out["probabilities"]=[{c:float(v) for c,v in zip(classes,row)} for row in probs]
        except Exception: pass
        return out
