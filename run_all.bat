@echo off
title StressGuard AI - System Launcher
echo ========================================================
echo Launching Real-Time Multimodal Stress Detection System
echo ========================================================
echo.
echo 1. Starting Backend Server in new window (Port 8000)...
start "StressGuard Backend (FastAPI)" cmd /k "%~dp0run_backend.bat"

echo 2. Waiting 2 seconds for API initialization...
timeout /t 2 /nobreak >nul

echo 3. Starting Frontend Server in new window (Port 5555)...
start "StressGuard Frontend (React)" cmd /k "%~dp0run_frontend.bat"

echo.
echo ========================================================
echo Both servers initiated!
echo Backend:  http://127.0.0.1:8000 (Docs: /docs)
echo Frontend: http://localhost:5555
echo Demo Account: demo@stressguard.edu / Demo@123
echo ========================================================
pause
