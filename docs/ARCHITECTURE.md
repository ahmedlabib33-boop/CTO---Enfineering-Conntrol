# Architecture

This repository implements the first production-usable vertical slice of the master platform:

DXF upload → immutable storage → parse → canonical entities → compare → Class A/B/C → approval → real DXF edit → reopen/QA → PDF/redline/XLSX.

The backend is FastAPI + SQLAlchemy + SQLite for the local MVP. The database layer can be migrated to PostgreSQL later. The web UI is Next.js.

## Engineering control boundary

Project-specific contract/design evidence is authoritative. The included rule file is a conservative default, not a substitute for project requirements. Class C is blocked from ordinary automatic approval at the API layer.
