\
from __future__ import annotations
from math import hypot
from .rules import classify

def _centroid(e: dict):
    c = e.get("centroid") or [0.0, 0.0, 0.0]
    return float(c[0]), float(c[1])

def _dist(a: dict, b: dict) -> float:
    ax, ay = _centroid(a)
    bx, by = _centroid(b)
    return hypot(ax-bx, ay-by)

def _shape_signature(e: dict) -> tuple:
    t = e.get("type")
    if t == "LINE":
        return (t, round(float(e.get("length", 0)), 4))
    if t in {"CIRCLE", "ARC"}:
        return (t, round(float(e.get("radius", 0)), 4))
    if t in {"LWPOLYLINE", "POLYLINE"}:
        return (t, len(e.get("points", [])), bool(e.get("closed", False)))
    if t in {"TEXT", "MTEXT"}:
        return (t, e.get("text", ""))
    if t == "INSERT":
        return (t, e.get("block_name", ""))
    return (t,)

def _equal_geometry(a: dict, b: dict) -> bool:
    ignore = {"handle", "layer", "text", "attributes"}
    aa = {k:v for k,v in a.items() if k not in ignore}
    bb = {k:v for k,v in b.items() if k not in ignore}
    return aa == bb

def compare_entities(current: list[dict], reference: list[dict], tolerance: float = 1e-4) -> list[dict]:
    changes = []
    cur_by_handle = {e.get("handle"): e for e in current if e.get("handle")}
    ref_by_handle = {e.get("handle"): e for e in reference if e.get("handle")}
    matched_cur, matched_ref = set(), set()

    # Handle is only a first-pass hint, never the sole matcher.
    for h, a in cur_by_handle.items():
        b = ref_by_handle.get(h)
        if b and a.get("type") == b.get("type"):
            matched_cur.add(id(a)); matched_ref.add(id(b))
            changes.extend(_diff_pair(a, b, tolerance))

    # Secondary geometric/context matcher
    for a in current:
        if id(a) in matched_cur:
            continue
        candidates = [b for b in reference if id(b) not in matched_ref and b.get("type") == a.get("type")]
        if not candidates:
            continue
        candidates.sort(key=lambda b: (_shape_signature(a) != _shape_signature(b), _dist(a,b), b.get("layer") != a.get("layer")))
        b = candidates[0]
        if _shape_signature(a) == _shape_signature(b) or _dist(a,b) <= max(tolerance, 1.0):
            matched_cur.add(id(a)); matched_ref.add(id(b))
            changes.extend(_diff_pair(a, b, tolerance, confidence="MEDIUM"))

    for a in current:
        if id(a) not in matched_cur:
            cc, auth = classify("DELETED")
            changes.append(_change("DELETED", a, None, cc, auth, "HIGH"))

    for b in reference:
        if id(b) not in matched_ref:
            cc, auth = classify("ADDED")
            changes.append(_change("ADDED", None, b, cc, auth, "HIGH"))

    for i, c in enumerate(changes, 1):
        c["change_key"] = f"C{i:04d}"
    return changes

def _diff_pair(a: dict, b: dict, tolerance: float, confidence="HIGH") -> list[dict]:
    out = []
    if a.get("layer") != b.get("layer"):
        cc, auth = classify("LAYER_CHANGED")
        out.append(_change("LAYER_CHANGED", a, b, cc, auth, confidence))
    if a.get("text") != b.get("text") and ("text" in a or "text" in b):
        cc, auth = classify("TEXT_CHANGED")
        out.append(_change("TEXT_CHANGED", a, b, cc, auth, confidence))
    if not _equal_geometry(a,b):
        d = _dist(a,b)
        ctype = "MOVED" if d > tolerance and _shape_signature(a) == _shape_signature(b) else "GEOMETRY_CHANGED"
        if a.get("type") == "DIMENSION":
            ctype = "DIMENSION_CHANGED"
        cc, auth = classify(ctype)
        out.append(_change(ctype, a, b, cc, auth, confidence))
    return out

def _change(change_type, a, b, change_class, authority, confidence):
    return {
        "change_type": change_type,
        "change_class": change_class,
        "authority": authority,
        "source_handle": (a or {}).get("handle", ""),
        "target_handle": (b or {}).get("handle", ""),
        "before": a or {},
        "after": b or {},
        "confidence": confidence,
        "status": "PENDING",
    }
