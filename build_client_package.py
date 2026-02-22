#!/usr/bin/env python3
"""Create minimal client ZIP package - SIMPLIFIED VERSION"""

import os
import shutil
import zipfile
from pathlib import Path

def main():
    print("\n" + "=" * 70)
    print("Creating Minimal Client Package for Distribution")
    print("=" * 70 + "\n")
    
    project_dir = Path.cwd()
    zip_file = project_dir / "Voice-Auth-System-Client.zip"
    
    # Remove existing zip
    if zip_file.exists():
        zip_file.unlink()
        print(f"Removed old: {zip_file.name}\n")
    
    print("Creating ZIP file (please wait)...\n")
    
    # Files and directories to exclude
    exclude = {
        'vosk_model',
        '__pycache__',
        '.git',
        'logs',
        'CLIENT_PACKAGE',
        'TEMP_CLIENT',
        '.gitignore',
        'create_presentation.py',
        'test_auth_init.py',
        'test_vosk_load.py',
        'examples.py',
        'verify_startup.py',
        'verify_vosk_setup.py',
        'setup_helper.py',
        'create_client_package.py',
        'download_vosk_model.py',  # Client needs this but will get from git
    }
    
    file_count = 0
    total_size = 0
    
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        for root, dirs, files in os.walk(project_dir):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude]
            
            for file in files:
                filepath = Path(root) / file
                
                # Skip excluded files
                if file.endswith(('.pyc', '.log', '.db', '.pyo')):
                    continue
                if file in exclude:
                    continue
                
                # Get relative path
                relpath = filepath.relative_to(project_dir)
                
                # Add to zip
                zf.write(filepath, relpath)
                file_count += 1
                total_size += filepath.stat().st_size
    
    zip_size = zip_file.stat().st_size
    
    print("\n" + "=" * 70)
    print("✅ CLIENT PACKAGE CREATED SUCCESSFULLY!")
    print("=" * 70 + "\n")
    
    print(f"📦 Filename: {zip_file.name}")
    print(f"📊 File size: {zip_size / 1024 / 1024:.1f} MB")
    print(f"📈 Files included: {file_count}")
    print(f"📁 Uncompressed: {total_size / 1024 / 1024:.1f} MB")
    print(f"🗜️  Compression: {(1 - zip_size/total_size)*100:.1f}%\n")
    
    print("=" * 70)
    print("🚀 HOW TO SHARE WITH CLIENTS:")
    print("=" * 70 + "\n")
    
    print("1. Send this file to your client:")
    print(f"   📤 {zip_file.name}\n")
    
    print("2. Client extracts the ZIP file to a folder\n")
    
    print("3. Client opens the folder and runs:")
    print("   ⏹️  START.bat  (Windows Command Prompt)")
    print("   or: START.ps1 (PowerShell)\n")
    
    print("4. First run will:")
    print("   ⬇️  Download VOSK model (1.4GB, once only)")
    print("   📦 Install Python packages")
    print("   🎤 Launch the application\n")
    
    print("5. After first run:")
    print("   ⚡ Starts in 5-10 seconds\n")
    
    print("=" * 70 + "\n")
    

if __name__ == "__main__":
    main()
