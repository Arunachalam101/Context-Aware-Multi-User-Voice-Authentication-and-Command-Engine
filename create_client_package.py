#!/usr/bin/env python3
"""
Create minimal client delivery package
Excludes: vosk_model, logs, __pycache__, .git, etc.
Size: ~200MB (compressed), client downloads VOSK model on first run
"""

import os
import shutil
import zipfile
from pathlib import Path

# Define what to include/exclude
EXCLUDE_DIRS = {
    'vosk_model',
    '__pycache__',
    '.git',
    '.gitignore',
    'data/raw_audio',
    'data/processed_features',
    'logs',
    '.vscode',
    '.idea'
}

EXCLUDE_FILES = {
    '*.pyc',
    '*.log',
    '*.db',
    '.DS_Store',
    'Thumbs.db',
    'create_presentation.py',
    'verify_startup.py',
    'verify_vosk_setup.py',
    'test_auth_init.py',
    'test_vosk_load.py',
    'examples.py'
}

def should_include(path):
    """Check if path should be included"""
    parts = path.parts
    
    # Exclude certain directories
    for part in parts:
        if part in EXCLUDE_DIRS:
            return False
    
    # Exclude certain files
    for pattern in EXCLUDE_FILES:
        if path.name.endswith(pattern.replace('*', '')):
            return False
    
    return True

def create_minimal_package():
    """Create minimal client package"""
    print("=" * 70)
    print("Creating Minimal Client Package")
    print("=" * 70)
    print()
    
    project_dir = Path(__file__).parent
    package_dir = project_dir / "CLIENT_PACKAGE"
    zip_file = project_dir / "Voice-Auth-System-Client.zip"
    
    # Remove old package
    if package_dir.exists():
        shutil.rmtree(package_dir)
    if zip_file.exists():
        zip_file.unlink()
    
    # Create package directory
    package_dir.mkdir()
    
    # Copy files
    print("📁 Copying project files...")
    copied_files = 0
    total_size = 0
    
    for source_path in project_dir.rglob('*'):
        if not source_path.is_file():
            continue
        
        if not should_include(source_path):
            continue
        
        # Determine relative path
        rel_path = source_path.relative_to(project_dir)
        dest_path = package_dir / rel_path
        
        # Create parent directories
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file
        shutil.copy2(source_path, dest_path)
        copied_files += 1
        total_size += dest_path.stat().st_size
        
        print(f"  ✓ {rel_path}")
    
    print()
    print(f"📊 Copied {copied_files} files")
    print(f"📦 Size: {total_size / 1024 / 1024:.1f} MB (uncompressed)")
    print()
    
    # Create zip file
    print("📦 Creating zip file...")
    print("   (This may take 1-2 minutes)")
    print()
    
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for source_path in package_dir.rglob('*'):
            if not source_path.is_file():
                continue
            
            arcname = source_path.relative_to(package_dir)
            zf.write(source_path, arcname)
    
    zip_size = zip_file.stat().st_size
    compression_ratio = (1 - zip_size / total_size) * 100
    
    print()
    print("✅ Package created successfully!")
    print()
    print("=" * 70)
    print()
    print(f"📦 File: {zip_file.name}")
    print(f"📊 Size: {zip_size / 1024 / 1024:.1f} MB (compressed)")
    print(f"📈 Compression: {compression_ratio:.1f}%")
    print()
    print("=" * 70)
    print()
    print("🚀 CLIENT INSTALLATION INSTRUCTIONS:")
    print()
    print("1. Send this file to your client:")
    print(f"   {zip_file.name}")
    print()
    print("2. Client extracts the zip file")
    print()
    print("3. Client double-clicks:")
    print("   START.bat  (or START.ps1 for PowerShell)")
    print()
    print("4. Application starts automatically!")
    print()
    print("   On first run:")
    print("   - Python packages installed (if needed)")
    print("   - VOSK model downloaded (1.4GB, once only)")
    print("   - Application launches")
    print()
    print("   After first run:")
    print("   - Starts in 5-10 seconds")
    print()
    print("=" * 70)
    print()
    
    # Clean up package directory
    shutil.rmtree(package_dir)

if __name__ == "__main__":
    create_minimal_package()
