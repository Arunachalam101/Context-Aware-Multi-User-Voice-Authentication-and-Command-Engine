#!/usr/bin/env python3
"""
Build Client Distribution ZIP Package
Excludes: vosk_model, __pycache__, .git, large test files
Creates minimal ZIP for client distribution that auto-downloads VOSK on first run
"""

import zipfile
import os
from pathlib import Path
import sys

def build_client_zip():
    project_dir = Path(__file__).parent
    zip_path = project_dir / "Voice-Auth-System-Client.zip"
    
    # Directories to skip
    skip_dirs = {
        'vosk_model',      # Downloaded on first client run
        '__pycache__',     # Python cache
        '.git',            # Version control
        'logs',            # Log files
        'data',            # Raw data/processed features
        '.vscode',         # VS Code settings
        '__pycache__'      # Byte code
    }
    
    # File patterns to skip
    skip_files = {
        '.pyc', '.log', '.db', '.sqlite3', '.gitignore',
        'test_*.py', 'verify_*.py', 'create_presentation.py',
        'examples.py', '.env'
    }
    
    print("[*] Building client distribution package...")
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            total_size = 0
            file_count = 0
            
            for root, dirs, files in os.walk(project_dir):
                # Filter out directories to skip
                dirs[:] = [d for d in dirs if d not in skip_dirs]
                
                for file in files:
                    file_path = Path(root) / file
                    
                    # Skip by extension or name
                    if any(file.endswith(ext) for ext in skip_files):
                        continue
                    
                    # Skip specific filenames
                    if file in {'create_client_package.py', 'make_client_zip.py', 'build_client_zip.py'}:
                        continue
                    
                    # Skip __pycache__ files anyway
                    if '__pycache__' in str(file_path):
                        continue
                    
                    try:
                        relative_path = file_path.relative_to(project_dir)
                        zipf.write(file_path, relative_path)
                        file_count += 1
                        total_size += file_path.stat().st_size
                        print(f"  + {relative_path}")
                    except Exception as e:
                        print(f"  [!] Skipped {file}: {e}")
        
        # Get final ZIP size
        zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
        print(f"\n[OK] Package created successfully!")
        print(f"   Location: {zip_path}")
        print(f"   Files: {file_count}")
        print(f"   Size: {zip_size_mb:.1f} MB")
        print(f"\n[INFO] To deploy:")
        print(f"   1. Extract ZIP to client folder")
        print(f"   2. Run: START.bat")
        print(f"   3. System auto-installs dependencies and downloads VOSK (~1.4GB)")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error creating ZIP: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = build_client_zip()
    sys.exit(0 if success else 1)
