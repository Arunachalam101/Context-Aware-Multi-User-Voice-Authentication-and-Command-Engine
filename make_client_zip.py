#!/usr/bin/env python3
"""Create minimal client package - WHITELIST approach"""

import os
import zipfile
from pathlib import Path

def main():
    print("\n" + "=" * 70)
    print("Creating Minimal Client Package (~200MB)")
    print("=" * 70 + "\n")
    
    project_dir = Path.cwd()
    zip_file = project_dir / "Voice-Auth-System-Client.zip"
    
    print("Building ZIP file...\n")
    
    file_count = 0
    total_size = 0
    
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
        for root, dirs, files in os.walk(project_dir):
            # Get relative path from project root
            rel_root = Path(root).relative_to(project_dir)
            root_str = str(rel_root).lower()
            
            # SKIP these directories completely
            if any(skip in root_str for skip in ['vosk_model', '__pycache__', '.git', 'client_package']):
                dirs.clear()  # Don't recurse into these
                continue
            
            # Process each file
            for file in files:
                filepath = Path(root) / file
                file_lower = file.lower()
                
                # SKIP certain files
                if any(skip in file_lower for skip in ['.pyc', '.log', '.db', '.pyo']):
                    continue
                
                # Especially skip large helper scripts
                if file in ['create_presentation.py', 'test_auth_init.py', 'test_vosk_load.py', 
                           'examples.py', 'verify_startup.py', 'verify_vosk_setup.py']:
                    continue
                
                # ADD the file
                relpath = filepath.relative_to(project_dir)
                zf.write(filepath, relpath)
                file_count += 1
                total_size += filepath.stat().st_size
                print(f"  + {relpath}")
    
    zip_size = zip_file.stat().st_size
    
    print("\n" + "=" * 70)
    print("✅ CLIENT PACKAGE READY FOR DISTRIBUTION!")
    print("=" * 70 + "\n")
    
    print(f"📦 Filename: {zip_file.name}")
    print(f"📊 Size: {zip_size / 1024 / 1024:.1f} MB (compressed)")
    print(f"📁 Files: {file_count}")
    print(f"🗜️  Compression: {(1 - zip_size/total_size)*100:.1f}%\n")
    
    print("=" * 70)
    print("🚀 SHARE THIS WITH YOUR CLIENT:")
    print("=" * 70 + "\n")
    
    print("File to send:")
    print(f"  📤 {zip_file.name}\n")
    
    print("Client instructions:")
    print("  1. Extract the ZIP to a folder")
    print("  2. Double-click: START.bat")
    print("  3. Wait for first-time setup (downloads VOSK model, ~1.4GB)")
    print("  4. Application starts automatically!\n")
    
    print("  After first run, it starts in 5-10 seconds\n")
    
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
