# CAD Engine

`apps/api/app/services/cad.py` uses `ezdxf`.

Supported parsing:
LINE, LWPOLYLINE, POLYLINE, ARC, CIRCLE, TEXT, MTEXT, INSERT, ATTRIB, DIMENSION, HATCH.

Supported automatic mutation in this MVP:
LINE, CIRCLE, ARC, LWPOLYLINE, TEXT, MTEXT plus deletion and selected additions.

Every export is reopened before success is returned.
