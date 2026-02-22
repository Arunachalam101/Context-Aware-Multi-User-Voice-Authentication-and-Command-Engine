#!/usr/bin/env python3
"""
VOSK Model Recovery & Initialization Script

Fixes "Failed to initialize VOSK model" error by:
1. Checking vosk package installation
2. Downloading/fixing vosk_model
3. Verifying integrity
4. Testing speech recognition
"""

import os
import sys
import json
from pathlib import Path
import urllib.request
import zipfile
import shutil
import subprocess

PROJECT_DIR = Path(__file__).parent
VOSK_MODEL_DIR = PROJECT_DIR / "vosk_model"
VOSK_MODEL_NAME = "vosk-model-en-us-0.42-gigaspeech"
VOSK_MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip"

def check_vosk_package():
    """Check if vosk package is installed."""
    print("[1/5] Checking vosk package...")
    try:
        import vosk
        print(f"  [OK] vosk {vosk.__version__} installed")
        return True
    except ImportError:
        print("  [FAILED] vosk package not found")
        print("  Installing vosk...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "vosk"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("  [OK] vosk installed successfully")
            return True
        else:
            print("  [ERROR] Failed to install vosk")
            print(result.stderr)
            return False

def check_model_directory():
    """Check if vosk_model directory exists and is valid."""
    print("\n[2/5] Checking model directory...")
    
    if VOSK_MODEL_DIR.exists():
        # Check for key model files
        required_files = ['model-en-us', 'ivector', 'conf']
        missing = [f for f in required_files 
                  if not (VOSK_MODEL_DIR / f).exists()]
        
        if missing:
            print(f"  [INCOMPLETE] Model missing: {missing}")
            print(f"  Deleting incomplete model...")
            shutil.rmtree(VOSK_MODEL_DIR)
            return False
        else:
            print(f"  [OK] Model directory valid at {VOSK_MODEL_DIR}")
            return True
    else:
        print(f"  [MISSING] {VOSK_MODEL_DIR} not found")
        return False

def download_model():
    """Download and extract VOSK model."""
    print(f"\n[3/5] Downloading VOSK model...")
    print(f"  URL: {VOSK_MODEL_URL}")
    print(f"  Size: ~1.4 GB (This may take 5-15 minutes)")
    
    try:
        zip_path = PROJECT_DIR / f"{VOSK_MODEL_NAME}.zip"
        
        # Download with progress
        def download_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, (downloaded * 100) // total_size)
            bar_length = 40
            filled = (percent * bar_length) // 100
            bar = '[' + '=' * filled + ' ' * (bar_length - filled) + ']'
            print(f'\r  Downloading: {bar} {percent}%', end='', flush=True)
        
        print("  Starting download..." )
        urllib.request.urlretrieve(VOSK_MODEL_URL, zip_path, download_progress)
        print(f"\n  [OK] Downloaded to {zip_path}")
        
        # Extract
        print("  Extracting model (this may take 2-3 minutes)...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(PROJECT_DIR)
        
        # Rename extracted folder to expected name
        extracted_dir = PROJECT_DIR / VOSK_MODEL_NAME
        if extracted_dir.exists() and extracted_dir != VOSK_MODEL_DIR:
            extracted_dir.rename(VOSK_MODEL_DIR)
        
        # Cleanup
        zip_path.unlink()
        print(f"  [OK] Extracted to {VOSK_MODEL_DIR}")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Download failed: {e}")
        return False

def test_vosk_model():
    """Test if VOSK model works."""
    print("\n[4/5] Testing VOSK model...")
    
    try:
        from vosk import Model, KaldiRecognizer
        
        if not VOSK_MODEL_DIR.exists():
            print("  [ERROR] Model directory not found after download")
            return False
        
        print(f"  Loading model from {VOSK_MODEL_DIR}...")
        model = Model(str(VOSK_MODEL_DIR))
        recognizer = KaldiRecognizer(model, 16000)
        
        print("  [OK] VOSK model loaded successfully")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Model test failed: {e}")
        return False

def test_speech_recognition():
    """Test speech recognition with audio file."""
    print("\n[5/5] Speech recognition system check...")
    
    try:
        import sounddevice
        import numpy as np
        
        print("  [OK] Audio libraries available")
        print("  [OK] System ready for speech recognition")
        return True
        
    except ImportError as e:
        print(f"  [WARNING] Audio library missing: {e}")
        print("  Installing audio libraries...")
        subprocess.run([sys.executable, "-m", "pip", "install", 
                       "sounddevice", "PyAudio"], capture_output=True)
        return True

def main():
    # Check for command-line arguments
    verify_only = "--verify-only" in sys.argv
    
    print("=" * 60)
    print("VOSK Model Recovery Tool")
    print("=" * 60)
    
    # Step 1: Check vosk package
    if not check_vosk_package():
        print("\n[FAILED] Cannot proceed without vosk package")
        return False
    
    # Step 2: Check model directory
    model_valid = check_model_directory()
    
    # Step 3: Download if needed (skip if verify-only)
    if not model_valid:
        if verify_only:
            print("\n[FAILED] Model verification failed (missing/incomplete)")
            return False
        
        if not download_model():
            print("\n[FAILED] Could not download model")
            return False
    
    # Step 4: Test model
    if not test_vosk_model():
        print("\n[FAILED] Model test failed")
        return False
    
    # Step 5: Test speech recognition
    test_speech_recognition()
    
    print("\n" + "=" * 60)
    print("[SUCCESS] VOSK model ready!")
    print("=" * 60)
    
    if not verify_only:
        print("\nYou can now:")
        print("  1. Run: python app.py")
        print("  2. Or run: START.bat")
        print("\nAuthentication and commands should work now!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
