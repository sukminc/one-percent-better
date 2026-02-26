# Action Tracker: The 1% Dashboard

A specialized poker analytics platform designed to transform raw GGPoker hand history logs into actionable behavioral insights. The goal is to facilitate a "1% better every day" growth trajectory by comparing current play against historical data with high-fidelity HUD statistics.

## Project Vision
To provide a modern, industrial-grade dashboard for poker players to identify leaks, analyze positional performance, and track growth over time.

## Key Features
- **Modern Dashboard**: High-fidelity UI with glassmorphism and smooth animations.
- **Drag & Drop Ingestion**: Dropbox-style hand history upload system.
- **Hero-Specific HUD**: VPIP, PFR, 3-Bet, C-Bet, Aggression Factor (AF), and Showdown stats (WTSD, W$SD).
- **Positional Intelligence**: Deep dive into performance across all table seats (Button, Blinds, UTG/MP/CO).
- **Data Visualization**: Interactive bar charts and radar matrices for behavioral analysis.

## Tech Stack
- **Frontend**: Next.js, TypeScript, Tailwind CSS, Framer Motion, Recharts, Lucide React.
- **Backend**: FastAPI (Python), SQLAlchemy, SQLite, Pydantic.
- **Parser**: Custom regex-based state-tracking engine for GGPoker logs.

## Quick Start

### Backend (API)
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.

### Frontend (UI)
```bash
cd frontend
npm install
npm run dev
```
The dashboard will be available at `http://localhost:3000`.

## Directory Structure
```
backend/          # FastAPI service, parser, and analytics
  app/
    main.py       # API entrypoint & routes
    parser.py     # GGPoker log parsing logic
    analytics.py  # HUD stat calculation engine
    db.py         # SQLAlchemy models & DB config
    models.py     # Pydantic schemas
  tests/          # Unit and integration tests
frontend/         # Next.js React dashboard
  pages/          # UI routes and components
testdata/         # (Git ignored) Local hand-history logs for testing
```

## Testing
Run backend tests:
```bash
cd backend
PYTHONPATH=. pytest
```

---
© 2026 ONE PERCENT BETTER. All rights reserved.
