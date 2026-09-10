\
from __future__ import annotations
from math import hypot
from typing import Any

NUMERIC_KEYS = (
    "length", "area", "radius", "height", "rotation", "start_angle", "end_angle"
)

def _f(v: Any, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return default

def _centroid(obj: dict) -> tuple[float, float]:
    c = obj.get("centroid") or obj.get("insert") or obj.get("center") or [0.0, 0.0]
    return _f(c[0]), _f(c[1])

def change_features(change: dict) -> dict[str, float | str]:
    """Create stable, non-project-secret feature primitives from a change record."""
    before = change.get("before") or {}
    after = change.get("after") or {}
    bx, by = _centroid(before)
    ax, ay = _centroid(after)
    out: dict[str, float | str] = {
        "change_type": str(change.get("change_type", "UNKNOWN")),
        "entity_type_before": str(before.get("type", "NONE")),
        "entity_type_after": str(after.get("type", "NONE")),
        "layer_before": str(before.get("layer", "NONE")),
        "layer_after": str(after.get("layer", "NONE")),
        "same_layer": float(before.get("layer") == after.get("layer")),
        "same_type": float(before.get("type") == after.get("type")),
        "movement_distance": hypot(ax-bx, ay-by),
        "text_changed": float(before.get("text") != after.get("text")),
        "block_changed": float(before.get("block_name") != after.get("block_name")),
        "attribute_changed": float(before.get("attributes") != after.get("attributes")),
        "point_count_before": float(len(before.get("points", []) or [])),
        "point_count_after": float(len(after.get("points", []) or [])),
    }
    for key in NUMERIC_KEYS:
        b = _f(before.get(key))
        a = _f(after.get(key))
        out[f"{key}_before"] = b
        out[f"{key}_after"] = a
        out[f"{key}_delta"] = a-b
        out[f"{key}_abs_delta"] = abs(a-b)
    return out
