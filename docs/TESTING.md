# Testing

From the repository root after the Python environment is installed:

```bash
python scripts/create_fixture.py
pytest -q
```

The core test proves parse → compare → approve → real DXF modification → reopen → QA.
