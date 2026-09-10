from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd, joblib
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from ..ml.classical_workbench import TabularMLWorkbench

class PlanningMLHub:
    TASKS={
        'activity_classification':('classification','random_forest'),
        'productivity_prediction':('regression','random_forest'),
        'crew_recommendation':('classification','random_forest'),
        'duration_risk':('classification','random_forest'),
        'criticality_risk':('classification','logistic'),
        'logic_assistance':('classification','random_forest'),
        'constructability_risk':('classification','random_forest'),
        'procurement_risk':('classification','random_forest'),
        'engineering_approval_risk':('regression','random_forest'),
    }
    def __init__(self, base_dir): self.base=Path(base_dir); self.base.mkdir(parents=True,exist_ok=True)
    def train(self, task_name, records, target, **kwargs):
        if task_name not in self.TASKS: raise ValueError('Unsupported planning ML task')
        task,model=self.TASKS[task_name]
        wb=TabularMLWorkbench(self.base/task_name)
        result=wb.train(records,target=target,task=task,model=kwargs.pop('model',model),**kwargs)
        result['planning_task']=task_name; result['governance']='ADVISORY_ONLY_HUMAN_REVIEW'; return result
    def predict(self, task_name, model_id, records, confidence_threshold=0.70):
        if task_name not in self.TASKS: raise ValueError('Unsupported planning ML task')
        out=TabularMLWorkbench(self.base/task_name).predict(model_id,records)
        out['planning_task']=task_name; out['authority']='ML_RECOMMENDATION_ONLY'
        probs=out.get('probabilities')
        if probs:
            gates=[]
            for row in probs:
                conf=max(row.values()) if row else 0.0
                gates.append({'confidence':conf,'status':'RECOMMEND' if conf>=confidence_threshold else 'ABSTAIN_REVIEW_REQUIRED'})
            out['confidence_gate']=gates
        return out
    def anomaly(self, records, columns=None, contamination='auto'):
        df=pd.DataFrame.from_records(records)
        if columns: df=df[columns]
        df=df.select_dtypes(include=[np.number,'bool'])
        if df.empty or len(df)<4: return {'status':'INSUFFICIENT_DATA','minimum_records':4}
        pipe=Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler()),('model',IsolationForest(contamination=contamination,random_state=42))])
        pred=pipe.fit_predict(df); score=pipe.decision_function(df)
        labels=['UNUSUAL' if p==-1 else 'NORMAL' for p in pred]
        return {'status':'COMPLETED','columns':df.columns.tolist(),'labels':labels,'scores':[float(x) for x in score],
                'governance':'ANOMALY_MEANS_REVIEW_REQUIRED_NOT_ERROR'}
