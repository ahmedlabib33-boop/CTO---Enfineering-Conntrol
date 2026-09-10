\
from pathlib import Path
import json
import ezdxf

ROOT=Path(__file__).resolve().parents[1]
FX=ROOT/"fixtures"; FX.mkdir(exist_ok=True)

doc=ezdxf.new("R2018"); doc.header["$INSUNITS"]=4
m=doc.modelspace()
m.add_line((0,0),(100,0),dxfattribs={"layer":"A-WALL"})
m.add_line((100,0),(100,50),dxfattribs={"layer":"A-WALL"})
m.add_circle((30,25),5,dxfattribs={"layer":"M-PIPE"})
t=m.add_text("ROOM 101",dxfattribs={"layer":"A-ANNO","height":2.5}); t.dxf.insert=(10,10)
doc.saveas(FX/"original.dxf")

rev=ezdxf.readfile(FX/"original.dxf"); rm=rev.modelspace()
ents=list(rm)
# moved circle
for e in ents:
    if e.dxftype()=="CIRCLE":
        e.dxf.center=(40,25)
# text change
for e in ents:
    if e.dxftype()=="TEXT":
        e.dxf.text="ROOM 102"
# delete vertical wall
for e in list(rm):
    if e.dxftype()=="LINE" and abs(e.dxf.start.x-100)<1e-9 and abs(e.dxf.end.x-100)<1e-9:
        rm.delete_entity(e)
# add line
rm.add_line((0,50),(100,50),dxfattribs={"layer":"A-WALL"})
rev.saveas(FX/"revised.dxf")

expected={"moved":1,"text_changed":1,"deleted":1,"added":1}
(FX/"expected_changes.json").write_text(json.dumps(expected,indent=2),encoding="utf-8")
print("Fixtures created:", FX)
