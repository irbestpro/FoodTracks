#!/bin/bash
set -e

# -------------------------------
# Quick Start Script: Backend + Frontend
# -------------------------------

# 1. Navigate to backend folder
cd ./BackEnd || { echo "BackEnd folder not found"; exit 1; }

# 2. Activate Python virtual environment
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment not found. Please create it first (python -m venv venv)."
    exit 1
fi

# 3. Run Alembic migrations (upgrade head)
echo "Applying Alembic migrations..."
python -m alembic upgrade head

# 4. Start FastAPI backend in background
echo "Starting FastAPI backend..."
python -m uvicorn Main:app --reload &

# 5. Open frontend in a new terminal and start React Native
# Works on Linux with gnome-terminal. Adjust for MacOS (use 'open -a Terminal') or Windows accordingly.
echo "Starting frontend..."
gnome-terminal -- bash -c "
cd ../FrontEnd/fe || exit
npm start
exec bash
"

echo "Backend running on http://127.0.0.1:8000"
echo "Frontend terminal opened."
