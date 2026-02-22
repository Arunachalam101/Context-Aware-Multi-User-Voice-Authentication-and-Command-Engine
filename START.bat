@echo off
REM =====================================================================
REM Context-Aware Multi-User Voice Authentication and Command Engine
REM Professional Client Installer & Launcher
REM =====================================================================
REM This is a SINGLE FILE that clients can run - it downloads everything
REM and starts the application automatically!
REM =====================================================================

setlocal enabledelayedexpansion
title Voice Authentication System - Loading...

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Colors and formatting
cls
echo.
echo =====================================================================
echo.
echo   🎤 Voice Authentication System v1.0.0
echo.
echo   Initializing Application...
echo.
echo =====================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found
    echo.
    echo Installing Python 3.11...
    echo Please follow the installer prompts
    echo Make sure to check "Add Python to PATH"
    echo.
    powershell -Command "Start-Process 'https://www.python.org/downloads/' -UseShellExecute"
    timeout /t 5 /nobreak
    echo.
    echo After installing Python, run this file again.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python found: %PYTHON_VERSION%

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: pip not found
    echo.
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

REM Install or upgrade pip
echo.
echo Checking pip installation...
python -m pip install --upgrade pip --quiet

REM Install required packages
echo.
echo Installing required packages...
echo (This may take 2-3 minutes on first run)
echo.

python -m pip install ^
    vosk ^
    numpy ^
    scipy ^
    scikit-learn ^
    librosa ^
    pyttsx3 ^
    sounddevice ^
    pyaudio ^
    --quiet

if errorlevel 1 (
    echo ❌ Error installing packages
    echo.
    echo Troubleshooting:
    echo 1. Check your internet connection
    echo 2. Make sure you have at least 500MB free space
    echo 3. Run: pip install --upgrade pip
    echo.
    pause
    exit /b 1
)

echo ✓ All packages installed successfully
echo.

REM Check if vosk_model directory exists and is valid
if not exist "vosk_model\" (
    echo.
    echo Downloading VOSK speech model (1.4GB)...
    echo This happens only once and may take 5-10 minutes
    echo Please wait...
    echo.
    
    if not exist "download_vosk_model.py" (
        echo ERROR: download_vosk_model.py not found
        echo.
        echo Please ensure all project files are in the same folder
        pause
        exit /b 1
    )
    
    python download_vosk_model.py
    
    if errorlevel 1 (
        echo ERROR: Failed to download VOSK model
        echo.
        echo Running recovery script...
        python fix_vosk_model.py
        
        if errorlevel 1 (
            echo.
            echo FAILED: Could not setup VOSK model
            echo.
            echo Try:
            echo 1. Check your internet connection
            echo 2. Ensure you have at least 2GB free space
            echo 3. Restart your computer
            echo 4. Run START.bat again
            echo.
            pause
            exit /b 1
        )
    )
    
    echo VOSK model downloaded successfully
) else (
    echo ✓ VOSK model found
    echo.
    echo Verifying model integrity...
    python fix_vosk_model.py --verify-only
    
    if errorlevel 1 (
        echo Model verification failed
        echo Running recovery...
        python fix_vosk_model.py
        
        if errorlevel 1 (
            echo ERROR: Model recovery failed
            pause
            exit /b 1
        )
    )
)


echo.
echo ✓ All setup complete!
echo.
echo =====================================================================
echo.
echo   🎤 Launching Voice Authentication System...
echo.
echo =====================================================================
echo.

REM Launch the main application
python app.py

if errorlevel 1 (
    echo.
    echo ❌ Application encountered an error
    echo.
    echo Troubleshooting:
    echo 1. Close other applications (browsers, Discord, etc.)
    echo 2. Check that your microphone is connected
    echo 3. Ensure you have at least 500MB free memory
    echo 4. Restart your computer
    echo.
    echo For more help, see: CLIENT_QUICK_START.md
    echo.
    pause
)

echo.
echo ✓ Application closed
echo.
pause
