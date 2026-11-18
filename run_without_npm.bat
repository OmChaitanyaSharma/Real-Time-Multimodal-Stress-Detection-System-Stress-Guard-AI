@echo off
setlocal enabledelayedexpansion
title StressGuard AI - Launcher (No Node.js / npm Required)
echo ======================================================================
echo    StressGuard AI: Multimodal Stress Detection System Launcher
echo    Mode: Standalone (Python Standard Library + Built Frontend)
echo    Port: Frontend @ http://localhost:5555 ^| Backend @ http://127.0.0.1:8000
echo ======================================================================
echo.

REM 1. Identify Python environment
set "PYTHON_EXE=python"
if exist "%~dp0venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0venv\Scripts\python.exe"
    echo [OK] Using virtual environment Python: venv\Scripts\python.exe
) else (
    where python >nul 2>nul
    if %errorlevel% neq 0 (
        echo [ERROR] Python 3 was not found on your system PATH!
        echo Please install Python 3.10+ from https://www.python.org/downloads/
        echo Make sure to check "Add Python to PATH" during installation.
        pause
        exit /b 1
    )
    echo [INFO] Virtual environment not found. Checking system Python...
    python -c "import fastapi, uvicorn, torch, sklearn" >nul 2>nul
    if %errorlevel% neq 0 (
        echo [SETUP] First-time setup detected. Creating virtual environment and installing dependencies...
        python -m venv "%~dp0venv"
        set "PYTHON_EXE=%~dp0venv\Scripts\python.exe"
        echo [SETUP] Installing required Python libraries from requirements.txt...
        "%~dp0venv\Scripts\pip.exe" install --upgrade pip
        "%~dp0venv\Scripts\pip.exe" install -r "%~dp0requirements.txt"
        echo [SETUP] Dependencies successfully installed!
    )
)

echo.
echo [1/3] Starting FastAPI Backend API (127.0.0.1:8000)...
start "StressGuard Backend API" cmd /k "cd /d "%~dp0backend" && "%PYTHON_EXE%" -m uvicorn app.main:app --host 127.0.0.1 --port 8000"

echo [2/3] Waiting for backend service initialization...
timeout /t 3 /nobreak >nul

echo [3/3] Starting Python Static Web Server (Port 5555)...
start "StressGuard Web Frontend" cmd /k "cd /d "%~dp0" && "%PYTHON_EXE%" serve_frontend.py"

echo.
echo ======================================================================
echo    System successfully launched!
echo.
echo    - Frontend Dashboard: http://localhost:5555
echo    - Backend API Docs:   http://127.0.0.1:8000/docs
echo    - Demo Credentials:   demo@stressguard.edu / Demo@123
echo ======================================================================
echo.

REM Automatically open the browser
start http://localhost:5555

pause
