@echo off
echo ========================================
echo Starting Quiz Application Backend
echo ========================================
echo.

cd backend

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Check if database exists
if not exist "instance\quiz.db" (
    echo Database not found. Initializing...
    python init_db.py
    echo.
)

REM Start the backend server
echo Starting Flask backend server...
echo Backend will be available at http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
