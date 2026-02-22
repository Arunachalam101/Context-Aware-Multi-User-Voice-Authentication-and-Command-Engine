#!/usr/bin/env python3
"""
Pre-Download Python Packages for Offline Installation
Run this once on a machine with internet, then distribute with project
"""

import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
PACKAGES_DIR = PROJECT_DIR / "offline_packages"

PACKAGES = [
    'vosk',
    'numpy',
    'scipy',
    'scikit-learn',
    'librosa',
    'pyttsx3',
    'sounddevice',
    'PyAudio',
]

def download_packages():
    """Download packages for offline installation."""
    print("=" * 60)
    print("Python Package Downloader")
    print("=" * 60)
    print()
    print("This tool downloads all required packages for offline use.")
    print("You can then distribute them to clients without internet.")
    print()
    
    # Create packages directory
    PACKAGES_DIR.mkdir(exist_ok=True)
    print(f"Packages will be saved to: {PACKAGES_DIR}")
    print()
    
    # Download each package
    for i, package in enumerate(PACKAGES, 1):
        print(f"[{i}/{len(PACKAGES)}] Downloading {package}...")
        
        result = subprocess.run(
            [sys.executable, "-m", "pip", "download", 
             package, "-d", str(PACKAGES_DIR),
             "--no-deps"],  # Don't download dependencies (we'll do that)
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"  ✓ {package} downloaded")
        else:
            print(f"  ✗ Failed to download {package}")
            print(f"    Error: {result.stderr}")
    
    print()
    print("=" * 60)
    print(f"[OK] Packages downloaded to: {PACKAGES_DIR}")
    print("=" * 60)
    print()
    print("Next step:")
    print(f"1. ZIP the entire project (including {PACKAGES_DIR})")
    print("2. Distribute to clients")
    print("3. Clients run: install_from_offline.bat")
    print()

if __name__ == "__main__":
    download_packages()
