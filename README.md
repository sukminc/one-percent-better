# one-percent-better

Minimal scaffold for the Action Tracker project.

This repository contains a small backend service (FastAPI) for parsing poker
hand histories and running tests. Local hand-history exports should be kept
outside the repository (use `testdata/` locally and keep it in `.gitignore`).

Quick start (backend):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
# Action Tracker: The 1% Dashboard

## Project Vision
A specialized poker analytics platform designed to transform raw hand history logs into actionable behavioral insights. The goal is to facilitate a "1% better every day" growth trajectory by comparing current play against historical data.

The repo is structured as a monorepo:

```
backend/          # FastAPI service for parsing and analysis
  app/
    main.py       # entrypoint
    parser.py     # hand-history parsing logic
    models.py     # pydantic models
  requirements.txt
frontend/         # (to be added) React/Next.js dashboard
```

Basic startup steps (backend):

1. `cd backend`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `uvicorn app.main:app --reload`

A SQLite database (`action_tracker.db` by default) will be created automatically in the backend directory when the server starts.  
`POST /upload-log/` accepts a text file, parses it into hands, saves each hand row, and returns the count + generated IDs.


### Testing

Run backend unit tests with `pytest` from the `backend/` folder.  Sample tests cover the parser and CRUD helpers.


# Action Tracker: The 1% Dashboard

This repository holds a small FastAPI backend and parsing tools to turn raw GGPoker hand-history logs
into structured records for analytics.

Repo layout (local):

- `backend/` — FastAPI service, parser, models, and tests
- `testdata/` — (ignored) local hand-history fixtures for development

Quick start (backend):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run tests:

```bash
cd backend
PYTHONPATH=. pytest -q
```

Notes:

- Local raw hand-history exports should live in `testdata/` (this folder is ignored by git).
- CI runs are configured via `.github/workflows/python-tests.yml` to run the backend tests on push/PR.

If you want a different README text or more detail, tell me what to include and I'll update it.