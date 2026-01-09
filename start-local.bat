@echo off
REM Local Development Startup Script for Windows (Without Docker)

echo ==========================================
echo Starting Dailyfix Messaging (Local Mode)
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo Creating Python virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

REM Setup backend
echo Setting up backend...
cd backend
call venv\Scripts\activate.bat

if not exist "venv\.deps-installed" (
    echo Installing Python dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    type nul > venv\.deps-installed
)

REM Create vector store directory
if not exist "vector_store" mkdir vector_store

REM Start backend
echo Starting backend on http://localhost:8000
start "Backend" cmd /k "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
cd ..

REM Setup frontend
echo Setting up frontend...
cd frontend

if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
)

REM Create .env.local if it doesn't exist
if not exist ".env.local" (
    echo Creating .env.local...
    (
        echo NEXT_PUBLIC_MATRIX_SERVER=http://localhost:8008
        echo NEXT_PUBLIC_AI_BACKEND=http://localhost:8000
    ) > .env.local
)

REM Start frontend
echo Starting frontend on http://localhost:3000
start "Frontend" cmd /k "npm run dev"
cd ..

echo.
echo ==========================================
echo Services Started!
echo ==========================================
echo.
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo.
echo Close the terminal windows to stop services.
echo.
pause
