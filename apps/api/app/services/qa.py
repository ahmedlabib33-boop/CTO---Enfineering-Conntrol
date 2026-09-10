from pathlib import Path
import ezdxf

def run_qa(path: str | Path) -> dict:
    path = Path(path)
    checks = []
    try:
        doc = ezdxf.readfile(path)
        checks.append({"rule_id":"CAD-OPEN-001","status":"PASS","message":"DXF reopened successfully"})
    except Exception as exc:
        return {"status":"FAIL","checks":[{"rule_id":"CAD-OPEN-001","status":"FAIL","message":str(exc)}]}

    msp = doc.modelspace()
    entities = list(msp)
    checks.append({"rule_id":"CAD-ENT-001","status":"PASS" if entities else "FAIL","message":f"{len(entities)} model-space entities"})
    units = int(doc.header.get("$INSUNITS", 0) or 0)
    checks.append({"rule_id":"CAD-UNIT-001","status":"PASS" if units else "WARNING","message":f"INSUNITS={units}"})
    layers = [layer.dxf.name for layer in doc.layers]
    checks.append({"rule_id":"CAD-LAYER-001","status":"PASS" if layers else "FAIL","message":f"{len(layers)} layers"})
    zero = 0
    for e in entities:
        if e.dxftype() == "LINE":
            if e.dxf.start.isclose(e.dxf.end):
                zero += 1
    checks.append({"rule_id":"CAD-GEO-001","status":"PASS" if zero == 0 else "WARNING","message":f"zero-length LINE entities={zero}"})
    if any(c["status"] == "FAIL" for c in checks):
        status = "FAIL"
    elif any(c["status"] == "WARNING" for c in checks):
        status = "PASS_WITH_WARNINGS"
    else:
        status = "PASS"
    return {"status": status, "checks": checks}
