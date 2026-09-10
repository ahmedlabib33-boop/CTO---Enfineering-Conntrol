# Known Limitations

Implemented now:
- native DXF ingestion;
- model-space entity normalization;
- deterministic comparison for supported entity types;
- Class A/B/C gate;
- approved DXF modification for LINE, CIRCLE, ARC, LWPOLYLINE, TEXT and MTEXT;
- DXF reopen QA;
- basic PDF plotting;
- redline register PDF;
- XLSX change register;
- local authentication;
- one-click Windows bootstrap.

Not yet engineering-grade / not complete:
- native DWG writing;
- DGN/RVT/NWC/NWD editing;
- full vector-PDF-to-DXF reconstruction;
- raster OCR/symbol reconstruction;
- IFC BIM semantic persistence;
- full discipline-specific technical calculations;
- full multidiscipline clash/clearance solver;
- advanced QTO;
- production RBAC / SSO;
- production PostgreSQL/PostGIS deployment;
- enterprise queue/workers.

The application must not represent these as complete.
