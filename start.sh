#!/usr/bin/env bash
set -e

# Run database migrations from repo root (alembic.ini is here,
# prepend_sys_path=backend lets alembic find the app module)
alembic upgrade head

# Start the API server
cd backend
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
