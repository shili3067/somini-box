#!/bin/bash
echo "🌊 Starting OmniBox (Web WebApp)..."

# Trap Ctrl+C (SIGINT) and kill the frontend server gracefully
trap 'echo -e "\n⏹️ Closing OmniBox..."; kill $FRONTEND_PID 2>/dev/null; exit 0' INT TERM EXIT

echo "Starting frontend server..."
cd frontend
npm run dev &
FRONTEND_PID=$!

sleep 2

# Open browser (macOS/Linux)
if command -v xdg-open > /dev/null; then
  xdg-open http://localhost:5173
elif command -v open > /dev/null; then
  open http://localhost:5173
else
  echo "Please open http://localhost:5173 in your browser."
fi

echo "Starting backend API..."
cd ../backend

# Activate virtualenv natively for macOS/Linux
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
else
    echo "Warning: Virtual environment not found. Using system Python."
fi

# Fallback to python3 if python is not available (common on macOS)
if command -v python3 >/dev/null 2>&1; then
    python3 main.py
else
    python main.py
fi
