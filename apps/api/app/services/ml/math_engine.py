\
from __future__ import annotations
from math import hypot, sqrt
from typing import Iterable
import networkx as nx
import sympy as sp

class EngineeringMathEngine:
    """Exact/analytical layer used before probabilistic ML where the problem is expressible mathematically."""

    @staticmethod
    def euclidean_distance(a: Iterable[float], b: Iterable[float]) -> float:
        aa=list(a); bb=list(b)
        return sqrt(sum((float(x)-float(y))**2 for x,y in zip(aa,bb)))

    @staticmethod
    def polyline_length(points: list[list[float]]) -> float:
        return sum(hypot(float(b[0])-float(a[0]), float(b[1])-float(a[1])) for a,b in zip(points,points[1:]))

    @staticmethod
    def polygon_area(points: list[list[float]]) -> float:
        if len(points) < 3: return 0.0
        pts = points + [points[0]]
        return abs(sum(float(a[0])*float(b[1])-float(b[0])*float(a[1]) for a,b in zip(pts,pts[1:]))) / 2.0

    @staticmethod
    def symbolic_check(expression: str, substitutions: dict[str, float] | None = None) -> dict:
        expr = sp.sympify(expression)
        simplified = sp.simplify(expr)
        value = simplified.subs(substitutions or {})
        return {"expression":str(expr),"simplified":str(simplified),"value":str(value)}

    @staticmethod
    def dependency_impact(edges: list[tuple[str,str]], changed: str, max_depth: int = 8) -> dict:
        g=nx.DiGraph(); g.add_edges_from(edges)
        impacted=[]
        if changed in g:
            lengths=nx.single_source_shortest_path_length(g, changed, cutoff=max_depth)
            impacted=sorted(({"node":n,"depth":d} for n,d in lengths.items() if n!=changed), key=lambda x:(x["depth"],x["node"]))
        return {"changed":changed,"impacted":impacted}

    @staticmethod
    def z3_constraint_check(constraints: list[dict]) -> dict:
        try:
            from z3 import Real, Solver, sat
        except Exception:
            return {"status":"CAPABILITY_UNAVAILABLE","library":"z3-solver"}
        vars={}
        s=Solver()
        for c in constraints:
            name=c["variable"]; op=c["op"]; val=float(c["value"])
            v=vars.setdefault(name, Real(name))
            if op==">=": s.add(v>=val)
            elif op=="<=": s.add(v<=val)
            elif op==">": s.add(v>val)
            elif op=="<": s.add(v<val)
            elif op=="==": s.add(v==val)
            else: raise ValueError(f"Unsupported op {op}")
        result=s.check()
        if result != sat: return {"status":str(result)}
        m=s.model()
        return {"status":"sat","solution":{n:str(m.eval(v, model_completion=True)) for n,v in vars.items()}}

    @staticmethod
    def optimize_integer(objective: list[int], upper_bounds: list[int], capacity: int) -> dict:
        try:
            from ortools.sat.python import cp_model
        except Exception:
            return {"status":"CAPABILITY_UNAVAILABLE","library":"ortools"}
        model=cp_model.CpModel()
        xs=[model.new_int_var(0,int(ub),f"x{i}") for i,ub in enumerate(upper_bounds)]
        model.add(sum(xs) <= int(capacity))
        model.maximize(sum(int(c)*x for c,x in zip(objective,xs)))
        solver=cp_model.CpSolver(); status=solver.solve(model)
        return {"status":solver.status_name(status),"x":[solver.value(x) for x in xs],"objective":solver.objective_value}
