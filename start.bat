@echo off
echo Starting OmniBox (Geek Toolbox)...

rem Start frontend development server in a new window/background
echo Starting frontend server...
cd frontend
start /B npm run dev > nul 2>&1
cd ..

rem Wait a moment for Vite to boot up
timeout /T 2 /NOBREAK > nul

rem Automatically open system default web browser
start http://localhost:5173

rem Start Python backend API
echo Starting backend API...
cd backend
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found.
)

python main.py

rem Once the Python server is graciously stopped (Ctrl+C), kill Node.
echo Closing OmniBox...
taskkill /F /IM node.exe > nul 2>&1

