# Engineering CAD Platform — Controlled DXF MVP

A real, runnable first vertical slice of the Technical Engineering CAD Modification Platform.

## What works

- Local admin login.
- Project creation.
- Immutable DXF upload with SHA-256.
- DXF parsing via `ezdxf`.
- Canonical entity records.
- Comparison using handle hints plus secondary geometry/context matching.
- Added / deleted / moved / geometry / text / layer change detection.
- Externalized Class A/B/C rule configuration.
- Server-side Class C approval block.
- Apply approved changes to a COPY of the current DXF.
- Reopen and QA the generated DXF.
- Generate revised PDF, redline PDF and XLSX change register.
- Audit records.
- One-click Windows startup.

## One-click start

On Windows, double-click:

`run_app.bat`

Prerequisites:
- Python 3.11+
- Node.js LTS for the Next.js UI

The launcher automatically installs declared Python and npm dependencies. It does not install system runtimes silently.

## Manual backend test

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python scripts\create_fixture.py
cd apps\api
..\..\..\.venv\Scripts\python -m uvicorn app.main:app --reload
```

Open `/docs`.

## Demo credentials

- Username: `admin`
- Password: `admin`

## Automated tests

```bash
.venv\Scripts\python scripts\create_fixture.py
.venv\Scripts\python -m pytest -q
```

## Demo files

`fixtures/original.dxf` and `fixtures/revised.dxf` are deterministic and contain:
- one moved entity;
- one text change;
- one deletion;
- one addition.

## Engineering boundary

Class C is not auto-approved. Generic knowledge does not override project-specific contract/design authority. See `docs/LIMITATIONS.md`.

## ML + mathematical intelligence

The upgraded package adds a project-scoped adaptive classifier, reviewed-feedback learning loop, symbolic mathematics, graph-impact analysis, and a capability registry for classical ML, boosting, deep learning, GNN, constraint optimization, SMT, Bayesian inference, CV and 3D geometry.

`run_app.bat` installs the mandatory ML/math dependency pack automatically. Heavy/hardware-sensitive packages are attempted separately and do not cause a false success if unavailable.

The ML layer is advisory: project authority, hard constraints and Class C approval gates remain authoritative.

The attached engineering knowledge base is packaged under `knowledge/` and indexed locally on first API startup. Use `/knowledge/search` for evidence retrieval. Generic knowledge remains advisory and cannot override project-specific governing documents.

## Construction Planning / Primavera layer

A second governed domain layer is now included for evidence-first schedule engineering, deterministic duration math, procurement need-date analysis, schedule QA, AACE schedule-basis/constructability review, XER staging creation, native-P6 verification boundaries, and planning-specific ML risk/recommendation tasks. Open `/planning` in the web UI. See `docs/PLANNING_PRIMAVERA_LAYER_V3.md`.
