@echo off
title WoodArt FRONTEND (puerto 5001)
cd /d "%~dp0"
".venv\Scripts\python.exe" -m src.app
pause
