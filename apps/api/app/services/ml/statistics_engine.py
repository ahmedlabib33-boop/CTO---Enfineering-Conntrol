from __future__ import annotations
from math import sqrt
from typing import Iterable
import numpy as np

class StatisticsMathEngine:
    @staticmethod
    def vector(values: Iterable[float]) -> np.ndarray:
        return np.asarray(list(values), dtype=float)

    @staticmethod
    def matrix(rows: Iterable[Iterable[float]]) -> np.ndarray:
        return np.asarray([list(r) for r in rows], dtype=float)

    @staticmethod
    def dot(a: Iterable[float], b: Iterable[float]) -> float:
        return float(np.dot(StatisticsMathEngine.vector(a), StatisticsMathEngine.vector(b)))

    @staticmethod
    def matmul(a, b):
        return np.matmul(StatisticsMathEngine.matrix(a), StatisticsMathEngine.matrix(b)).tolist()

    @staticmethod
    def mean(values) -> float:
        return float(np.mean(StatisticsMathEngine.vector(values)))

    @staticmethod
    def variance(values, sample: bool=False) -> float:
        return float(np.var(StatisticsMathEngine.vector(values), ddof=1 if sample else 0))

    @staticmethod
    def stddev(values, sample: bool=False) -> float:
        return sqrt(StatisticsMathEngine.variance(values, sample))

    @staticmethod
    def covariance(x, y, sample: bool=True) -> float:
        a,b=StatisticsMathEngine.vector(x),StatisticsMathEngine.vector(y)
        if len(a)!=len(b): raise ValueError("x and y must have equal length")
        return float(np.cov(a,b,ddof=1 if sample else 0)[0,1])

    @staticmethod
    def correlation(x, y) -> float:
        a,b=StatisticsMathEngine.vector(x),StatisticsMathEngine.vector(y)
        if len(a)!=len(b): raise ValueError("x and y must have equal length")
        return float(np.corrcoef(a,b)[0,1])

    @staticmethod
    def conditional_probability(joint_count: float, condition_count: float) -> float:
        if condition_count <= 0: raise ValueError("condition_count must be > 0")
        return float(joint_count/condition_count)

    @staticmethod
    def bayes_posterior(prior: float, likelihood: float, evidence: float) -> float:
        if evidence <= 0: raise ValueError("evidence must be > 0")
        if not all(0 <= v <= 1 for v in (prior, likelihood, evidence)):
            raise ValueError("probabilities must be between 0 and 1")
        return float(likelihood*prior/evidence)

    @staticmethod
    def normal_pdf(x: float, mean: float=0.0, std: float=1.0) -> float:
        if std <= 0: raise ValueError("std must be > 0")
        z=(x-mean)/std
        return float(np.exp(-0.5*z*z)/(std*np.sqrt(2*np.pi)))

    @staticmethod
    def gradient_descent_linear_regression(x, y, learning_rate: float=0.01, iterations: int=1000) -> dict:
        X,Y=StatisticsMathEngine.vector(x),StatisticsMathEngine.vector(y)
        if len(X)!=len(Y) or len(X)==0: raise ValueError("x and y must be equal non-empty")
        m=b=0.0
        n=float(len(X))
        history=[]
        for i in range(int(iterations)):
            pred=m*X+b
            err=pred-Y
            m-=learning_rate*float((2/n)*np.dot(err,X))
            b-=learning_rate*float((2/n)*np.sum(err))
            if i in {0,iterations-1} or (iterations>=10 and i % max(1,iterations//10)==0):
                history.append({"iteration":i,"mse":float(np.mean((m*X+b-Y)**2))})
        return {"slope":float(m),"intercept":float(b),"mse":float(np.mean((m*X+b-Y)**2)),"history":history}
