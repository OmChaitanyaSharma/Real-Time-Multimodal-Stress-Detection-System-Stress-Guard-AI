@echo off
title StressGuard AI - Backend Server (Port 8000)
echo ========================================================
echo Starting FastAPI Backend Server on http://127.0.0.1:8000
echo Interactive API Documentation: http://127.0.0.1:8000/docs
echo ========================================================
cd /d "%~dp0backend"
..\venv\Scripts\uvicorn.exe app.main:app --host 127.0.0.1 --port 8000 --reload
pause
