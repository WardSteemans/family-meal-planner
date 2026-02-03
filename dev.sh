#!/bin/bash
set -e

echo "🐳 Starting Database (Docker)..."
docker compose up -d db

echo "⏳ Waiting for DB..."
sleep 2

echo "🚀 Starting Backend (FastAPI)..."
# We gaan even de backend map in om de venv te activeren en te starten
cd backend
source .venv/bin/activate

# Omdat we nu IN de map 'backend' zitten, ziet uvicorn de map 'app' direct liggen
uvicorn app.main:app --reload
