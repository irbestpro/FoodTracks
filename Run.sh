#!/bin/bash
# Exit on any error
set -e

echo "Starting database migrations..."

# (Optional) Activate virtual environment
# source ./BackEnd/venv/bin/activate

# Navigate to backend folder
cd ./BackEnd

# Generate Alembic migration
echo "Generating new Alembic migration..."
python -m alembic revision --autogenerate -m "DB Initialization"

# Apply migrations
echo "Applying migrations..."
python -m alembic upgrade head

# Start backend (FastAPI)
echo "Starting FastAPI backend..."
uvicorn main:app --reload &

# Navigate to frontend folder
cd ../FrontEnd/fe

# Start frontend
echo "Starting frontend..."
npm start
