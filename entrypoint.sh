#!/bin/sh
# Use environment variable WORKERS (default to 1 if not set)
WORKERS=${WORKERS:-1}
PORT=${PORT:-8000}
echo "Starting uvicorn with $WORKERS worker(s)..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$PORT" --workers "$WORKERS"