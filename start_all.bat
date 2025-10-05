@echo off
echo ========================================
echo Starting Quiz Application
echo ========================================
echo.
echo This will start both backend and frontend servers
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Press any key to continue...
pause > nul

REM Start backend in new window
start "Quiz Backend" cmd /k "cd /d %~dp0 && start_backend.bat"

REM Wait a bit for backend to start
timeout /t 3 /nobreak > nul

REM Start frontend in new window
start "Quiz Frontend" cmd /k "cd /d %~dp0 && start_frontend.bat"

echo.
echo Both servers are starting in separate windows...
echo.
pause
