@echo off
title WeatherGlass - Starting...
color 0A

echo.
echo  =========================================
echo    WeatherGlass - Auto Launcher
echo  =========================================
echo.

:: ── Go to the folder where this .bat file lives ──
cd /d "%~dp0"

echo  [1/3] Checking Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo  ERROR: Python not found. Install from python.org
    pause
    exit
)
echo  Python found.

echo.
echo  [2/3] Installing dependencies...
pip install flask flask-cors requests >nul 2>&1
echo  Dependencies ready.

echo.
echo  [3/3] Starting Flask backend...
echo.
echo  =========================================
echo    App running at: http://localhost:5000
echo    Close this window to STOP the server.
echo  =========================================
echo.

:: ── Wait 2 seconds then open browser automatically ──
timeout /t 2 /nobreak >nul
start http://localhost:5000

:: ── Start Flask server ──
python server.py

pause