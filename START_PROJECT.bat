@echo off
REM =====================================================================
REM Context-Aware Multi-User Voice Authentication and Command Engine
REM Professional Startup Script for Client Deployment
REM =====================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

REM Clear screen and show banner
cls
echo.
echo =====================================================================
echo.
echo   🎤 Voice Authentication System
echo.
echo   Starting Application...
echo.
echo =====================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.9+ from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import vosk, tkinter, numpy, sounddevice" >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Required packages are missing
    echo.
    echo Installing required packages...
    pip install vosk tkinter numpy sounddevice pyaudio scipy
    if errorlevel 1 (
        echo Failed to install packages. Please check your internet connection.
        pause
        exit /b 1
    )
)

REM Launch the application with safe startup
echo.
echo ✓ All requirements verified
echo.
echo Starting application with resource monitoring...
echo.
timeout /t 2 /nobreak >nul

python run_safe.py

if errorlevel 1 (
    echo.
    echo ❌ Application exited with an error
    echo.
    echo Troubleshooting tips:
    echo 1. Close other applications (browsers, Discord, etc.)
    echo 2. Check your microphone is connected and enabled
    echo 3. Restart your computer if experiencing issues
    echo.
    pause
    exit /b 1
)

echo.
echo ✓ Application closed successfully
echo.
pause
