#!/usr/bin/env python3
"""
VOSK Model Diagnostic Tool
Identifies why "Failed to create a model" error occurs
"""

import os
import sys
from pathlib import Path
import json

PROJECT_DIR = Path(__file__).parent
VOSK_MODEL_DIR = PROJECT_DIR / "vosk_model"

def check_model_structure():
    """Check if model has all required files and directories."""
    print("[1/4] Checking model structure...\n")
    
    if not VOSK_MODEL_DIR.exists():
        print(f"  [ERROR] Model directory not found: {VOSK_MODEL_DIR}")
        return False
    
    # Required directories and files
    required = {
        'directories': ['am-english', 'conf', 'graph', 'ivector'],
        'critical_files': [
            'am-english/final.mdl',
            'conf/mfcc.conf',
            'graph/HCLG.fst',
            'graph/words.txt',
            'ivector/final.ie',
            'ivector/final.mat'
        ]
    }
    
    print(f"  Model path: {VOSK_MODEL_DIR}")
    print(f"  Model exists: {VOSK_MODEL_DIR.exists()}")
    print(f"  Model size: {sum(f.stat().st_size for f in VOSK_MODEL_DIR.glob('**/*') if f.is_file()) / (1024**3):.2f} GB\n")
    
    missing_dirs = []
    for req_dir in required['directories']:
        dir_path = VOSK_MODEL_DIR / req_dir
        status = "✓" if dir_path.exists() else "✗"
        print(f"  {status} {req_dir}/")
        if not dir_path.exists():
            missing_dirs.append(req_dir)
    
    print()
    missing_files = []
    for req_file in required['critical_files']:
        file_path = VOSK_MODEL_DIR / req_file
        status = "✓" if file_path.exists() else "✗"
        print(f"  {status} {req_file}")
        if not file_path.exists():
            missing_files.append(req_file)
    
    all_ok = len(missing_dirs) == 0 and len(missing_files) == 0
    
    if not all_ok:
        print(f"\n  [PROBLEM] Missing directories: {missing_dirs}")
        print(f"  [PROBLEM] Missing files: {missing_files}")
        print(f"\n  This means the model extraction was INCOMPLETE")
        print(f"  Solution: Delete and re-download the model")
        return False
    
    print(f"\n  [OK] All required files present")
    return True

def check_file_permissions():
    """Check if model files are readable."""
    print("\n[2/4] Checking file permissions...\n")
    
    try:
        # Try to read a critical file
        test_files = [
            VOSK_MODEL_DIR / 'conf' / 'mfcc.conf',
            VOSK_MODEL_DIR / 'graph' / 'HCLG.fst',
        ]
        
        for test_file in test_files:
            if test_file.exists():
                try:
                    with open(test_file, 'rb') as f:
                        data = f.read(100)
                    print(f"  ✓ Can read: {test_file.relative_to(PROJECT_DIR)}")
                except PermissionError:
                    print(f"  ✗ Permission denied: {test_file.relative_to(PROJECT_DIR)}")
                    print(f"    Try: chmod 644 {test_file}")
                    return False
                except Exception as e:
                    print(f"  ✗ Error reading: {test_file} - {e}")
                    return False
        
        print(f"\n  [OK] All files readable")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Permission check failed: {e}")
        return False

def check_vosk_library():
    """Check if VOSK library can import Model."""
    print("\n[3/4] Checking VOSK library...\n")
    
    try:
        from vosk import Model, KaldiRecognizer
        print(f"  ✓ vosk.Model imported successfully")
        print(f"  ✓ vosk.KaldiRecognizer imported successfully")
        
        # Try to create model
        print(f"\n  Attempting to load model from {VOSK_MODEL_DIR}...")
        try:
            model = Model(str(VOSK_MODEL_DIR))
            print(f"  ✓ Model loaded successfully!")
            
            # Try to create recognizer
            rec = KaldiRecognizer(model, 16000)
            print(f"  ✓ Recognizer created successfully!")
            return True
            
        except Exception as e:
            print(f"  ✗ Model creation failed: {e}")
            print(f"\n  Error details:")
            print(f"  - Type: {type(e).__name__}")
            print(f"  - Message: {str(e)}")
            
            if "Failed to create a model" in str(e):
                print(f"\n  This usually means:")
                print(f"  1. Model files are corrupted")
                print(f"  2. Model directory is incomplete")
                print(f"  3. VOSK version incompatibility")
            
            return False
            
    except ImportError as e:
        print(f"  ✗ vosk library error: {e}")
        print(f"  Try: pip install --upgrade vosk")
        return False
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
        return False

def diagnose():
    """Run all diagnostics."""
    print("=" * 60)
    print("VOSK Model Diagnostic")
    print("=" * 60)
    print()
    
    struct_ok = check_model_structure()
    perm_ok = check_file_permissions()
    vosk_ok = check_vosk_library()
    
    print("\n" + "=" * 60)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 60)
    print(f"  Model structure: {'✓ OK' if struct_ok else '✗ FAILED'}")
    print(f"  File permissions: {'✓ OK' if perm_ok else '✗ FAILED'}")
    print(f"  VOSK library: {'✓ OK' if vosk_ok else '✗ FAILED'}")
    
    if struct_ok and perm_ok and vosk_ok:
        print("\n[SUCCESS] Model is ready to use!")
        return True
    else:
        print("\n[SOLUTION] Run this command to fix:")
        print("  python fix_vosk_model.py")
        print("\nOr manually:")
        print("  1. Delete model: Remove-Item vosk_model -Recurse -Force")
        print("  2. Re-download: python download_vosk_model.py")
        print("  3. Verify: python diagnose_vosk.py")
        return False

if __name__ == "__main__":
    success = diagnose()
    sys.exit(0 if success else 1)
