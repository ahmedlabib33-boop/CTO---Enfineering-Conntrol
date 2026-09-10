\
from pathlib import Path
import json, math
import ezdxf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from openpyxl import Workbook
from .cad import entity_record

def _bounds(entities):
    xs, ys = [], []
    for e in entities:
        r = entity_record(e)
        for key in ("start","end","center","insert","centroid"):
            if key in r:
                xs.append(float(r[key][0])); ys.append(float(r[key][1]))
        for p in r.get("points", []):
            xs.append(float(p[0])); ys.append(float(p[1]))
    if not xs:
        return (0,0,100,100)
    return min(xs), min(ys), max(xs), max(ys)

def dxf_to_pdf(dxf_path: str | Path, pdf_path: str | Path, title="Revised Drawing") -> str:
    doc = ezdxf.readfile(dxf_path)
    ents = list(doc.modelspace())
    x0,y0,x1,y1 = _bounds(ents)
    page = landscape(A3)
    w,h = page
    margin = 36
    sx = (w-2*margin) / max(x1-x0, 1)
    sy = (h-2*margin) / max(y1-y0, 1)
    s = min(sx, sy)
    def tx(x): return margin + (x-x0)*s
    def ty(y): return margin + (y-y0)*s
    pdf_path = Path(pdf_path); pdf_path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(pdf_path), pagesize=page)
    c.setTitle(title)
    c.drawString(margin, h-24, title)
    for e in ents:
        t = e.dxftype()
        if t == "LINE":
            c.line(tx(e.dxf.start.x), ty(e.dxf.start.y), tx(e.dxf.end.x), ty(e.dxf.end.y))
        elif t == "CIRCLE":
            c.circle(tx(e.dxf.center.x), ty(e.dxf.center.y), abs(e.dxf.radius*s))
        elif t == "ARC":
            r=abs(e.dxf.radius*s)
            c.arc(tx(e.dxf.center.x)-r, ty(e.dxf.center.y)-r, tx(e.dxf.center.x)+r, ty(e.dxf.center.y)+r,
                  startAng=e.dxf.start_angle, extent=(e.dxf.end_angle-e.dxf.start_angle))
        elif t == "LWPOLYLINE":
            pts=list(e.get_points("xy"))
            if len(pts)>=2:
                p=c.beginPath(); p.moveTo(tx(pts[0][0]),ty(pts[0][1]))
                for q in pts[1:]: p.lineTo(tx(q[0]),ty(q[1]))
                if e.closed: p.close()
                c.drawPath(p)
        elif t == "TEXT":
            c.drawString(tx(e.dxf.insert.x), ty(e.dxf.insert.y), str(e.dxf.text)[:120])
        elif t == "MTEXT":
            c.drawString(tx(e.dxf.insert.x), ty(e.dxf.insert.y), e.plain_text()[:120])
    c.save()
    return str(pdf_path)

def change_register_xlsx(changes: list[dict], path: str | Path) -> str:
    wb = Workbook()
    ws = wb.active
    ws.title = "Change Register"
    headers = ["Change ID","Change Type","Class","Authority","Source Handle","Target Handle","Confidence","Status","Before","After"]
    ws.append(headers)
    for c in changes:
        ws.append([
            c.get("change_key"), c.get("change_type"), c.get("change_class"), c.get("authority"),
            c.get("source_handle"), c.get("target_handle"), c.get("confidence"), c.get("status"),
            json.dumps(c.get("before",{}), ensure_ascii=False), json.dumps(c.get("after",{}), ensure_ascii=False)
        ])
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(path)
    return str(path)

def redline_pdf(changes: list[dict], path: str | Path) -> str:
    page = landscape(A3)
    w,h = page
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(path), pagesize=page)
    c.setTitle("Redline Change Register")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(36,h-36,"Engineering CAD Redline / Difference Register")
    y=h-70
    c.setFont("Helvetica", 9)
    for ch in changes:
        line=f"{ch.get('change_key')} | {ch.get('change_type')} | Class {ch.get('change_class')} | {ch.get('status')} | {ch.get('source_handle')} -> {ch.get('target_handle')}"
        c.drawString(36,y,line[:180])
        y-=14
        if y<36:
            c.showPage(); y=h-36; c.setFont("Helvetica",9)
    c.save()
    return str(path)
