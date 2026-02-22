@echo off
REM Safe startup script for Voice Authentication System
REM Run this instead of app.py to prevent crashes

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo.
echo ================================================================
echo Voice Authentication System - SAFE STARTUP
echo ================================================================
echo.
echo This script will:
echo   1. Check system resources
echo   2. Verify application components
echo   3. Start the application safely
echo.
echo If you experience crashes:
echo   - Close other applications (browsers, Discord, etc.)
echo   - Run: diagnose_system.py
echo   - Restart your computer
echo.

REM Run with memory monitoring
python run_safe.py

REM Check exit code
if errorlevel 1 (
    echo.
    echo Application failed to start
    pause
    exit /b 1
)
