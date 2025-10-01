#!/bin/bash
# start.sh - start backend and frontend in parallel

cleanup() {
    echo "Stopping all processes..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Trap CTRL+C (SIGINT) and other exit signals
trap cleanup SIGINT SIGTERM EXIT


start_backend() {
    echo "Starting backend..."
    cd backend || exit

    uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

start_frontend() {
    echo "Starting frontend..."
    cd frontend || exit

    pnpm run dev
}


start_backend &
BACKEND_PID=$!

start_frontend &
FRONTEND_PID=$!

wait -n $BACKEND_PID $FRONTEND_PID

cleanup