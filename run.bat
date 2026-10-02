@echo off
REM Double-click to start Document Editor (after the one-time setup in README.md)
cd /d "%~dp0"
if exist .venv\Scripts\pythonw.exe (
    start "" .venv\Scripts\pythonw.exe main.py %*
) else (
    echo The .venv folder was not found. Do the setup steps in README.md first.
    pause
)
