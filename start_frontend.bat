@echo off
echo ========================================
echo Starting Quiz Application Frontend
echo ========================================
echo.

cd frontend

REM Check if node_modules exists
if not exist "node_modules\" (
    echo Installing dependencies...
    call npm install
    echo.
)

REM Start the development server
echo Starting Vite development server...
echo Frontend will be available at http://localhost:3000
echo.
echo Press Ctrl+C to stop the server
echo.
call npm run dev

pause
