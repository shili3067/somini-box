#!/bin/bash
echo "Starting OmniVid Downloader (Web App)..."

echo "Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!

sleep 2

# Open browser (macOS/Linux)
if which xdg-open > /dev/null; then
  xdg-open http://localhost:5173
elif which open > /dev/null; then
  open http://localhost:5173
fi

echo "Starting backend API..."
cd ../backend

if [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

python main.py

echo "Closing OmniVid Downloader..."
kill $FRONTEND_PID

