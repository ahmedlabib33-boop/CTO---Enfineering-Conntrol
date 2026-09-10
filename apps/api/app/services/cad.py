\
from __future__ import annotations
from pathlib import Path
from math import hypot
import json
import ezdxf

SUPPORTED = {
    "LINE", "LWPOLYLINE", "POLYLINE", "ARC", "CIRCLE", "TEXT", "MTEXT",
    "INSERT", "ATTRIB", "DIMENSION", "HATCH"
}

def _round(v, n=6):
    try:
        return round(float(v), n)
    except Exception:
        return v

def _point(p):
    return [_round(p[0]), _round(p[1]), _round(p[2] if len(p) > 2 else 0.0)]

def entity_record(e) -> dict:
    t = e.dxftype()
    d = {
        "handle": str(getattr(e.dxf, "handle", "") or ""),
        "type": t,
        "layer": str(getattr(e.dxf, "layer", "0") or "0"),
    }
    if t == "LINE":
        d["start"] = _point(e.dxf.start)
        d["end"] = _point(e.dxf.end)
        d["centroid"] = [(_round(e.dxf.start.x + e.dxf.end.x) / 2), (_round(e.dxf.start.y + e.dxf.end.y) / 2), 0.0]
        d["length"] = _round(hypot(e.dxf.end.x-e.dxf.start.x, e.dxf.end.y-e.dxf.start.y))
    elif t == "CIRCLE":
        d["center"] = _point(e.dxf.center)
        d["radius"] = _round(e.dxf.radius)
        d["centroid"] = d["center"]
    elif t == "ARC":
        d["center"] = _point(e.dxf.center)
        d["radius"] = _round(e.dxf.radius)
        d["start_angle"] = _round(e.dxf.start_angle)
        d["end_angle"] = _round(e.dxf.end_angle)
        d["centroid"] = d["center"]
    elif t == "LWPOLYLINE":
        pts = [[_round(p[0]), _round(p[1])] for p in e.get_points("xy")]
        d["points"] = pts
        d["closed"] = bool(e.closed)
        if pts:
            d["centroid"] = [_round(sum(x for x, _ in pts)/len(pts)), _round(sum(y for _, y in pts)/len(pts)), 0.0]
    elif t == "POLYLINE":
        pts = [[_round(v.dxf.location.x), _round(v.dxf.location.y)] for v in e.vertices]
        d["points"] = pts
        d["closed"] = bool(e.is_closed)
        if pts:
            d["centroid"] = [_round(sum(x for x, _ in pts)/len(pts)), _round(sum(y for _, y in pts)/len(pts)), 0.0]
    elif t == "TEXT":
        d["text"] = str(e.dxf.text)
        d["insert"] = _point(e.dxf.insert)
        d["centroid"] = d["insert"]
        d["height"] = _round(getattr(e.dxf, "height", 0))
    elif t == "MTEXT":
        d["text"] = e.plain_text()
        d["insert"] = _point(e.dxf.insert)
        d["centroid"] = d["insert"]
    elif t == "INSERT":
        d["block_name"] = str(e.dxf.name)
        d["insert"] = _point(e.dxf.insert)
        d["centroid"] = d["insert"]
        d["attributes"] = {a.dxf.tag: a.dxf.text for a in e.attribs}
    elif t == "ATTRIB":
        d["tag"] = str(e.dxf.tag)
        d["text"] = str(e.dxf.text)
        d["insert"] = _point(e.dxf.insert)
        d["centroid"] = d["insert"]
    elif t == "DIMENSION":
        d["dimtype"] = int(getattr(e.dxf, "dimtype", 0))
        d["text"] = str(getattr(e.dxf, "text", ""))
        d["defpoint"] = _point(e.dxf.defpoint)
        d["centroid"] = d["defpoint"]
    elif t == "HATCH":
        d["solid_fill"] = int(getattr(e.dxf, "solid_fill", 0))
        d["centroid"] = [0.0, 0.0, 0.0]
    else:
        d["centroid"] = [0.0, 0.0, 0.0]
    return d

def parse_dxf(path: str | Path) -> dict:
    path = Path(path)
    doc = ezdxf.readfile(path)
    msp = doc.modelspace()
    entities = []
    unsupported = []
    for e in msp:
        if e.dxftype() in SUPPORTED:
            try:
                entities.append(entity_record(e))
            except Exception as exc:
                unsupported.append({"type": e.dxftype(), "handle": str(getattr(e.dxf, "handle", "")), "error": str(exc)})
        else:
            unsupported.append({"type": e.dxftype(), "handle": str(getattr(e.dxf, "handle", ""))})
    units = int(doc.header.get("$INSUNITS", 0) or 0)
    layers = [layer.dxf.name for layer in doc.layers]
    return {
        "file": str(path),
        "dxfversion": doc.dxfversion,
        "units_code": units,
        "layers": layers,
        "entity_count": len(entities),
        "unsupported": unsupported,
        "entities": entities,
    }

def _find_by_handle(msp, handle: str):
    for e in msp:
        if str(getattr(e.dxf, "handle", "") or "") == str(handle):
            return e
    return None

def _copy_from_reference(target_msp, ref_entity):
    t = ref_entity.dxftype()
    if t == "LINE":
        return target_msp.add_line(ref_entity.dxf.start, ref_entity.dxf.end, dxfattribs={"layer": ref_entity.dxf.layer})
    if t == "CIRCLE":
        return target_msp.add_circle(ref_entity.dxf.center, ref_entity.dxf.radius, dxfattribs={"layer": ref_entity.dxf.layer})
    if t == "ARC":
        return target_msp.add_arc(ref_entity.dxf.center, ref_entity.dxf.radius, ref_entity.dxf.start_angle, ref_entity.dxf.end_angle, dxfattribs={"layer": ref_entity.dxf.layer})
    if t == "LWPOLYLINE":
        return target_msp.add_lwpolyline(list(ref_entity.get_points("xy")), dxfattribs={"layer": ref_entity.dxf.layer, "closed": ref_entity.closed})
    if t == "TEXT":
        ne = target_msp.add_text(ref_entity.dxf.text, dxfattribs={"layer": ref_entity.dxf.layer, "height": getattr(ref_entity.dxf, "height", 2.5)})
        ne.dxf.insert = ref_entity.dxf.insert
        return ne
    if t == "MTEXT":
        ne = target_msp.add_mtext(ref_entity.text, dxfattribs={"layer": ref_entity.dxf.layer})
        ne.dxf.insert = ref_entity.dxf.insert
        return ne
    raise ValueError(f"ADD not implemented for {t}")

def apply_changes(current_path: str | Path, reference_path: str | Path, changes: list[dict], output_path: str | Path) -> str:
    current_path, reference_path, output_path = Path(current_path), Path(reference_path), Path(output_path)
    doc = ezdxf.readfile(current_path)
    ref = ezdxf.readfile(reference_path)
    msp = doc.modelspace()
    ref_msp = ref.modelspace()

    for ch in changes:
        if ch.get("status") != "APPROVED":
            continue
        ctype = ch["change_type"]
        src_handle = ch.get("source_handle", "")
        tgt_handle = ch.get("target_handle", "")
        if ctype == "ADDED":
            ref_entity = _find_by_handle(ref_msp, tgt_handle)
            if ref_entity is not None:
                _copy_from_reference(msp, ref_entity)
            continue
        src = _find_by_handle(msp, src_handle)
        if src is None:
            continue
        if ctype == "DELETED":
            msp.delete_entity(src)
            continue
        ref_entity = _find_by_handle(ref_msp, tgt_handle)
        if ref_entity is None:
            continue

        t = src.dxftype()
        if ctype in {"MOVED", "GEOMETRY_CHANGED", "TEXT_CHANGED", "LAYER_CHANGED"}:
            src.dxf.layer = ref_entity.dxf.layer
            if t == "LINE":
                src.dxf.start = ref_entity.dxf.start
                src.dxf.end = ref_entity.dxf.end
            elif t == "CIRCLE":
                src.dxf.center = ref_entity.dxf.center
                src.dxf.radius = ref_entity.dxf.radius
            elif t == "ARC":
                src.dxf.center = ref_entity.dxf.center
                src.dxf.radius = ref_entity.dxf.radius
                src.dxf.start_angle = ref_entity.dxf.start_angle
                src.dxf.end_angle = ref_entity.dxf.end_angle
            elif t == "LWPOLYLINE":
                src.set_points(list(ref_entity.get_points("xy")))
                src.closed = ref_entity.closed
            elif t == "TEXT":
                src.dxf.text = ref_entity.dxf.text
                src.dxf.insert = ref_entity.dxf.insert
            elif t == "MTEXT":
                src.text = ref_entity.text
                src.dxf.insert = ref_entity.dxf.insert

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(output_path)
    # independent reopen check
    ezdxf.readfile(output_path)
    return str(output_path)
