import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

class UnsupervisedEngineeringML:
    @staticmethod
    def _numeric(records, columns=None):
        df=pd.DataFrame.from_records(records)
        if columns:
            missing=[c for c in columns if c not in df.columns]
            if missing: raise ValueError(f"Missing columns: {missing}")
            df=df[columns]
        df=df.select_dtypes(include=[np.number,"bool"])
        if df.empty: raise ValueError("No numeric features available")
        return df

    @staticmethod
    def kmeans(records, clusters=3, columns=None, random_state=42):
        X=UnsupervisedEngineeringML._numeric(records,columns)
        k=max(2,min(int(clusters),len(X)))
        pipe=Pipeline([("imputer",SimpleImputer(strategy="median")),("scale",StandardScaler()),("cluster",KMeans(n_clusters=k,random_state=random_state,n_init="auto"))])
        labels=pipe.fit_predict(X)
        return {"method":"KMEANS","columns":X.columns.tolist(),"clusters":k,"labels":[int(v) for v in labels],"inertia":float(pipe.named_steps["cluster"].inertia_)}

    @staticmethod
    def pca(records, components=2, columns=None):
        X=UnsupervisedEngineeringML._numeric(records,columns)
        n=max(1,min(int(components),X.shape[1],len(X)))
        pipe=Pipeline([("imputer",SimpleImputer(strategy="median")),("scale",StandardScaler()),("pca",PCA(n_components=n))])
        transformed=pipe.fit_transform(X); pca=pipe.named_steps["pca"]
        return {"method":"PCA","columns":X.columns.tolist(),"components":n,"explained_variance_ratio":[float(v) for v in pca.explained_variance_ratio_],"transformed":transformed.tolist()}
