@echo off
title GitSentinel EDR App Launcher
echo Starting GitSentinel Universal EDR Desktop App...
cd /d "%~dp0"
python src/desktop_main.py
if errorlevel 1 (
    echo Python launch failed. Trying python3...
    python3 src/desktop_main.py
)
pause
