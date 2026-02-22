#!/usr/bin/env python3
"""
VOSK Model Downloader
Downloads and extracts the English VOSK speech recognition model
Model: vosk-model-en-us-0.42-gigaspeech (~1.4GB)
"""

import os
import sys
import urllib.request
import zipfile
from pathlib import Path

def download_vosk_model():
    """Download and extract VOSK model"""
    
    project_root = Path(__file__).parent
    model_dir = project_root / "vosk_model"
    
    print("=" * 70)
    print("VOSK MODEL DOWNLOADER")
    print("=" * 70)
    print()
    print(f"Project Root: {project_root}")
    print(f"Model Directory: {model_dir}")
    print()
    
    # Check if model already exists
    if model_dir.exists() and list(model_dir.glob("*")):
        print("✓ VOSK model already exists in vosk_model/")
        print("  Ready to proceed!")
        return True
    
    # Create vosk_model directory if it doesn't exist
    model_dir.mkdir(exist_ok=True)
    
    # Model download URL
    model_url = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip"
    model_file = model_dir / "vosk-model-en-us-0.42-gigaspeech.zip"
    
    print("MODEL DOWNLOAD DETAILS:")
    print("-" * 70)
    print(f"Model: English US (US English)")
    print(f"Size: ~1.4 GB (may take 10-30 minutes)")
    print(f"URL: {model_url}")
    print()
    print("DOWNLOAD OPTIONS:")
    print("-" * 70)
    print("1. Auto-download (this script)")
    print("2. Manual download (copy URL, download in browser)")
    print()
    
    choice = input("Choose option [1/2] (default=1): ").strip() or "1"
    
    if choice == "2":
        print()
        print("MANUAL DOWNLOAD INSTRUCTIONS:")
        print("-" * 70)
        print(f"1. Copy this URL: {model_url}")
        print("2. Open in browser or use a download manager")
        print(f"3. Save to: {model_dir}/vosk-model-en-us-0.42-gigaspeech.zip")
        print("4. Run this script again to auto-extract")
        print()
        return False
    
    # Auto-download
    if model_file.exists():
        print(f"✓ Model file already exists: {model_file.name}")
        extract_choice = input("Extract model? [y/n] (default=y): ").strip().lower() or "y"
        if extract_choice != "y":
            return False
    else:
        print()
        print("DOWNLOADING MODEL...")
        print("-" * 70)
        try:
            urllib.request.urlretrieve(
                model_url, 
                model_file,
                reporthook=show_progress
            )
            print()
            print(f"✓ Downloaded: {model_file.name}")
        except Exception as e:
            print(f"\n✗ Download failed: {e}")
            print()
            print("TROUBLESHOOTING:")
            print("- Check internet connection")
            print("- Try manual download (choose option 2)")
            print("- Visit: https://alphacephei.com/vosk/models")
            return False
    
    # Extract model
    print()
    print("EXTRACTING MODEL...")
    print("-" * 70)
    try:
        with zipfile.ZipFile(model_file, 'r') as zip_ref:
            zip_ref.extractall(model_dir)
        print(f"✓ Extracted to: {model_dir}/")
        
        # List extracted contents
        contents = list(model_dir.iterdir())
        print()
        print("CONTENTS:")
        for item in sorted(contents):
            if item.is_dir():
                print(f"  📁 {item.name}/")
            else:
                print(f"  📄 {item.name}")
        
        # Clean up zip file
        model_file.unlink()
        print()
        print(f"✓ Removed: {model_file.name}")
        
    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        return False
    
    return True

def show_progress(block_num, block_size, total_size):
    """Show download progress"""
    downloaded = block_num * block_size
    percent = min(downloaded * 100 / total_size, 100)
    mb_downloaded = downloaded / (1024 * 1024)
    mb_total = total_size / (1024 * 1024)
    
    bar_length = 50
    filled = int(bar_length * percent / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    print(f"\r[{bar}] {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end="")

def verify_model():
    """Verify model is ready"""
    project_root = Path(__file__).parent
    model_dir = project_root / "vosk_model"
    
    if not model_dir.exists():
        return False
    
    # Look for model directories (they vary by version)
    model_contents = list(model_dir.glob("*"))
    
    # Check for common VOSK model directory patterns
    has_model = any(
        item.is_dir() and (
            "vosk" in item.name.lower() or
            item.name.startswith("model")
        )
        for item in model_contents
    )
    
    return has_model or len(model_contents) > 0

if __name__ == "__main__":
    print()
    
    try:
        success = download_vosk_model()
        
        print()
        print("=" * 70)
        if success and verify_model():
            print("✓ VOSK MODEL SETUP COMPLETE!")
            print("=" * 70)
            print()
            print("You can now run: python app.py")
            print()
            sys.exit(0)
        elif success:
            print("✓ MODEL DOWNLOADED")
            print("=" * 70)
            print()
            print("Ready to use VOSK model!")
            print("Run: python app.py")
            print()
            sys.exit(0)
        else:
            print("⚠ MODEL SETUP INCOMPLETE")
            print("=" * 70)
            print()
            print("Please complete manual download if needed.")
            print()
            sys.exit(1)
            
    except KeyboardInterrupt:
        print()
        print()
        print("✓ Download cancelled by user")
        sys.exit(0)
    except Exception as e:
        print()
        print(f"✗ Error: {e}")
        sys.exit(1)
