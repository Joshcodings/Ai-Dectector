@echo off
title AI Image Detector — Backend Server
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   AI Image Detector — Starting Server    ║
echo  ╚══════════════════════════════════════════╝
echo.
echo  [INFO] Installing / verifying dependencies…
pip install -r requirements.txt --quiet
echo.
echo  [INFO] Starting FastAPI server on http://127.0.0.1:8000
echo  [INFO] Press Ctrl+C to stop.
echo.
cd /d "%~dp0"
uvicorn app:app --reload --host 0.0.0.0 --port 8000
pause
