@echo off
REM =====================================================================
REM Voice Authentication System - ONE-CLICK STARTER
REM =====================================================================
REM For Clients: Just double-click this file!
REM Everything else happens automatically.
REM =====================================================================

setlocal enabledelayedexpansion
title Voice Authentication System - Starting...
cls

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo.
echo =====================================================================
echo.
echo   Voice Authentication System
echo.
echo   Starting setup... please wait
echo.
echo =====================================================================
echo.

REM Step 1: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not installed
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    timeout /t 5 /nobreak
    exit /b 1
)

REM Step 2: Install packages (silent, continue even if already installed)
echo [1/3] Checking packages...
pip install -q vosk numpy scipy scikit-learn librosa pyttsx3 sounddevice PyAudio 2>nul

REM Check if pip install failed
if errorlevel 1 (
    echo.
    echo Retrying package installation...
    echo (Sometimes the first attempt fails due to network timeouts)
    echo.
    
    REM Retry with longer timeout
    pip install --default-timeout=1000 vosk numpy scipy scikit-learn librosa pyttsx3 sounddevice PyAudio
    
    if errorlevel 1 (
        echo.
        echo WARNING: Some packages failed to install
        echo.
        echo This usually means:
        echo 1. No internet connection
        echo 2. Network firewall blocking pip
        echo 3. Proxy/VPN blocking access
        echo.
        echo SOLUTIONS:
        echo 1. Check your internet connection
        echo 2. Try again in a few minutes
        echo 3. Disable VPN/Proxy temporarily
        echo 4. Use a different network (hotspot, workplace WiFi)
        echo.
        echo Continuing anyway - some features may not work...
    )
)

REM Step 3: Verify/download VOSK model
echo [2/3] Checking speech model...
if not exist "vosk_model\" (
    echo.
    echo Downloading speech recognition model (1.4 GB)...
    echo This happens ONLY ONCE - may take 5-15 minutes
    echo.
    
    if exist "fix_vosk_model.py" (
        python fix_vosk_model.py
    ) else if exist "download_vosk_model.py" (
        python download_vosk_model.py
    ) else (
        echo ERROR: Model download script not found
        pause
        exit /b 1
    )
    
    if errorlevel 1 (
        echo.
        echo ERROR: Could not download model
        echo.
        echo SOLUTIONS:
        echo 1. Check your internet connection
        echo 2. Ensure you have 2GB free disk space
        echo 3. Try running this file again
        echo.
        pause
        exit /b 1
    )
)

REM Step 4: Launch application
echo [3/3] Launching application...
echo.

python app.py

REM If app closes with error
if errorlevel 1 (
    echo.
    echo.
    echo ERROR: Application encountered a problem
    echo.
    echo Try:
    echo 1. Close other programs (browsers, Discord, etc.)
    echo 2. Restart your computer
    echo 3. Run this file again
    echo.
    pause
    exit /b 1
)

echo.
echo Application closed
pause

