@echo off
REM =====================================================================
REM Install from Offline Packages
REM Use this if RUN.bat fails due to internet/network issues
REM =====================================================================

setlocal enabledelayedexpansion
title Voice Authentication System - Offline Installation
cls

echo.
echo =====================================================================
echo. 
echo   Offline Package Installation
echo.
echo   Installing from local packages...
echo.
echo =====================================================================
echo.

REM Check if offline_packages folder exists
if not exist "offline_packages\" (
    echo ERROR: offline_packages folder not found!
    echo.
    echo This file is for offline installation only.
    echo If you have internet, run: RUN.bat
    echo.
    echo If the offline_packages folder is missing:
    echo 1. Download the full project ZIP again
    echo 2. Make sure it includes offline_packages folder
    echo.
    pause
    exit /b 1
)

REM Install from offline packages
echo Installing packages from offline_packages/...
echo This may take 2-3 minutes...
echo.

pip install --no-index --find-links="offline_packages" vosk numpy scipy scikit-learn librosa pyttsx3 sounddevice PyAudio

if errorlevel 1 (
    echo.
    echo ERROR: Installation failed
    echo.
    echo Possible solutions:
    echo 1. Make sure offline_packages folder has all files
    echo 2. Try: pip install --upgrade pip
    echo 3. Restart your computer and try again
    echo.
    pause
    exit /b 1
)

echo.
echo =====================================================================
echo.
echo   [OK] Packages installed successfully!
echo.
echo =====================================================================
echo.
echo Now you can run: RUN.bat
echo.
pause
