@echo off
title StressGuard AI - Frontend Server (Port 5555)
echo ========================================================
echo Starting React 19 Frontend on http://localhost:5555
echo (Port 5173 is preserved for Daily Tracker)
echo ========================================================
cd /d "%~dp0frontend"
npm run dev
pause
