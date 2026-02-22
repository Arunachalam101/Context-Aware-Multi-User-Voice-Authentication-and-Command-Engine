#!/usr/bin/env python3
"""
Build Client Distribution ZIP Package - SIMPLE VERSION
Uses explicit whitelist approach to avoid vosk_model
"""

import zipfile
import os
from pathlib import Path
import sys

def build_client_zip():
    project_dir = Path(__file__).parent
    zip_path = project_dir / "Voice-Auth-System-Client.zip"
    
    # Explicitly include only these root directories
    include_dirs = {
        'audio', 'commands', 'database', 'features', 'gui',
        'ml', 'models', 'response', 'speech', 'utils', 'offline_packages'  # New: Include offline packages if available
    }
    
    # Root Python files to include
    root_files = {
        'app.py', 'requirements.txt', 'README.md',
        'RUN.bat', 'START.bat', 'START.ps1', 'run.bat', 'run_safe.bat', 'run_safe.py',
        'INSTALL_OFFLINE.bat',  # New: Offline installation
        'safe_startup.py', 'setup_helper.py', 'download_vosk_model.py',
        'diagnose_system.py', 'test_microphone.py', 'fix_vosk_model.py', 'diagnose_vosk.py',
        'download_offline_packages.py',  # New: For offline package generation
        'CLIENT_QUICK_START.md', 'CLIENT_START_HERE.md', 'CLIENT_SETUP.txt',
        'COMPLETION_SUMMARY.md', 'DELIVERY_SUMMARY.md',
        'DEPLOYMENT.md', 'DEPLOYMENT_CHECKLIST.md', 'DEPLOYMENT_GUIDE.md',
        'DEVICE_RESTART_FIX.md', 'MANIFEST.md', 'PROJECT_STATUS.md',
        'QUICK_START.md', 'SCHEDULE.md', 'SPEECH_RECOGNITION_GUIDE.md',
        'START_HERE.md', 'START_HERE.txt', 'START_PROJECT.bat',
        'TEST_RESULTS.md', 'VOSK_INITIALIZATION_FIX.md', 'MODEL_CREATION_ERROR_FIX.md',
        'FRIEND_SETUP.md', 'CLIENT_NETWORK_SOLUTIONS.md',  # New: Network solutions guide
        'NETWORK_INSTALLATION_GUIDE.md', 'RUN_BAT_TROUBLESHOOTING.md'  # New: Troubleshooting guides
    }
    
    # Documentation files to include
    doc_extensions = {'.md', '.txt'}
    
    print("[*] Building client distribution package...")
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            total_size = 0
            file_count = 0
            
            # Add root files
            for root_file in root_files:
                root_path = project_dir / root_file
                if root_path.exists() and root_path.is_file():
                    try:
                        zipf.write(root_path, root_file)
                        file_count += 1
                        total_size += root_path.stat().st_size
                        print(f"  + {root_file}")
                    except Exception as e:
                        print(f"  [!] Skipped {root_file}: {e}")
            
            # Add subdirectories
            for subdir in include_dirs:
                subdir_path = project_dir / subdir
                if not subdir_path.exists():
                    continue
                    
                for root, dirs, files in os.walk(subdir_path):
                    # Skip __pycache__
                    dirs[:] = [d for d in dirs if d != '__pycache__']
                    
                    for file in files:
                        # Skip compiled Python files
                        if file.endswith('.pyc') or file.endswith('.log'):
                            continue
                        
                        file_path = Path(root) / file
                        try:
                            relative_path = file_path.relative_to(project_dir)
                            zipf.write(file_path, str(relative_path))
                            file_count += 1
                            total_size += file_path.stat().st_size
                            print(f"  + {relative_path}")
                        except Exception as e:
                            print(f"  [!] Skipped {file_path}: {e}")
        
        # Get final ZIP size
        zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
        print(f"\n[OK] Package created successfully!")
        print(f"   Location: {zip_path}")
        print(f"   Files: {file_count}")
        print(f"   Size: {zip_size_mb:.1f} MB")
        print(f"\n[INFO] To deploy:")
        print(f"   1. Extract ZIP to client folder")
        print(f"   2. Option A (Online): Run RUN.bat")
        print(f"   3. Option B (Offline): Run INSTALL_OFFLINE.bat (if offline_packages/ included)")
        print(f"   4. System auto-installs dependencies and downloads VOSK (~1.4GB) if needed")
        
        # Check if offline_packages is included
        offline_status = "[INCLUDED]" if (project_dir / "offline_packages").exists() else "[NOT INCLUDED - Run download_offline_packages.py to add]"
        print(f"\n[INFO] Offline packages: {offline_status}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error creating ZIP: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = build_client_zip()
    sys.exit(0 if success else 1)
