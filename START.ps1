#!/usr/bin/env powershell
<#
.SYNOPSIS
    Context-Aware Multi-User Voice Authentication and Command Engine
    Professional Client Installer & Launcher
    
.DESCRIPTION
    This is a SINGLE FILE script that clients can run.
    It automatically:
    - Checks Python installation
    - Installs required packages
    - Downloads VOSK speech model (on first run only)
    - Starts the application
    
.EXAMPLE
    Right-click START.ps1 → Run with PowerShell
#>

$ProgressPreference = 'SilentlyContinue'
$ErrorActionPreference = 'SilentlyContinue'

# Display banner
Clear-Host
Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  🎤 Voice Authentication System v1.0.0" -ForegroundColor Green
Write-Host ""
Write-Host "  Initializing Application..." -ForegroundColor Yellow
Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Set script location as working directory
Set-Location -Path $PSScriptRoot

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow

$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ERROR: Python not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installing Python 3.11..." -ForegroundColor Yellow
    Write-Host "Please follow the installer prompts" -ForegroundColor Yellow
    Write-Host "⚠️  Make sure to check 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host ""
    
    Start-Process "https://www.python.org/downloads/"
    
    Write-Host "After installing Python, run this file again." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Python found: $pythonCheck" -ForegroundColor Green

# Upgrade pip
Write-Host ""
Write-Host "Updating pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet --disable-warnings

# Install required packages
Write-Host ""
Write-Host "Installing required packages..." -ForegroundColor Yellow
Write-Host "(This may take 2-3 minutes on first run)" -ForegroundColor Gray
Write-Host ""

$packages = @(
    "vosk",
    "numpy",
    "scipy",
    "scikit-learn",
    "librosa",
    "pyttsx3",
    "sounddevice",
    "pyaudio"
)

foreach ($package in $packages) {
    Write-Host "  Installing $package..." -ForegroundColor Gray
    python -m pip install $package --quiet --disable-warnings
}

Write-Host ""
Write-Host "✓ All packages installed successfully" -ForegroundColor Green
Write-Host ""

# Check VOSK model
if (-not (Test-Path "vosk_model")) {
    Write-Host ""
    Write-Host "Downloading VOSK speech model (1.4GB)..." -ForegroundColor Yellow
    Write-Host "This happens only once and may take 5-10 minutes" -ForegroundColor Gray
    Write-Host ""
    
    if (-not (Test-Path "download_vosk_model.py")) {
        Write-Host "❌ ERROR: download_vosk_model.py not found" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please ensure all project files are in the same folder" -ForegroundColor Red
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    python download_vosk_model.py
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to download VOSK model" -ForegroundColor Red
        Write-Host ""
        Write-Host "Troubleshooting:" -ForegroundColor Yellow
        Write-Host "  1. Check your internet connection" -ForegroundColor Gray
        Write-Host "  2. Make sure you have at least 2GB free space" -ForegroundColor Gray
        Write-Host "  3. Try again" -ForegroundColor Gray
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    Write-Host "✓ VOSK model downloaded successfully" -ForegroundColor Green
}
else {
    Write-Host "✓ VOSK model already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "✓ All setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  🎤 Launching Voice Authentication System..." -ForegroundColor Green
Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Launch application
python app.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Application closed successfully" -ForegroundColor Green
    Write-Host ""
}
else {
    Write-Host ""
    Write-Host "❌ Application encountered an error" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Close other applications (browsers, Discord, etc.)" -ForegroundColor Gray
    Write-Host "  2. Check that your microphone is connected" -ForegroundColor Gray
    Write-Host "  3. Ensure you have at least 500MB free memory" -ForegroundColor Gray
    Write-Host "  4. Restart your computer" -ForegroundColor Gray
    Write-Host ""
    Write-Host "For more help, see: CLIENT_QUICK_START.md" -ForegroundColor Gray
    Write-Host ""
}

Read-Host "Press Enter to exit"
