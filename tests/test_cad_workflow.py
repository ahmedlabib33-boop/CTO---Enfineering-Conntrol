\
from pathlib import Path
import json, subprocess, sys
from app.services.cad import parse_dxf, apply_changes
from app.services.comparison import compare_entities
from app.services.qa import run_qa

ROOT=Path(__file__).resolve().parents[1]
FX=ROOT/"fixtures"

def ensure_fixtures():
    if not (FX/"original.dxf").exists():
        subprocess.check_call([sys.executable,str(ROOT/"scripts"/"create_fixture.py")])

def test_parse_compare_modify_qa(tmp_path):
    ensure_fixtures()
    original=parse_dxf(FX/"original.dxf")
    revised=parse_dxf(FX/"revised.dxf")
    assert original["entity_count"] == 4
    changes=compare_entities(original["entities"],revised["entities"])
    types=[c["change_type"] for c in changes]
    assert "MOVED" in types
    assert "TEXT_CHANGED" in types
    assert "DELETED" in types
    assert "ADDED" in types
    # Approve everything except any Class C
    for c in changes:
        if c["change_class"] != "C":
            c["status"]="APPROVED"
    out=tmp_path/"output.dxf"
    apply_changes(FX/"original.dxf",FX/"revised.dxf",changes,out)
    qa=run_qa(out)
    assert qa["status"] in {"PASS","PASS_WITH_WARNINGS"}
    reparsed=parse_dxf(out)
    assert reparsed["entity_count"] >= 1
