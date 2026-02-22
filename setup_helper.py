"""
Setup Helper Script - Guides users through initial configuration
Run this once before first use to set up the system.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    print("\n" + "="*70)
    print(f" {text}")
    print("="*70 + "\n")

def print_step(number, text):
    print(f"\n[STEP {number}] {text}")
    print("-" * 70)

def check_python_version():
    """Verify Python 3.8+"""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor} - UPGRADE REQUIRED (3.8+ needed)")
        return False

def check_dependencies():
    """Verify all Python packages are installed"""
    print_step(2, "Checking Dependencies")
    
    required_packages = {
        "sounddevice": "Audio recording",
        "soundfile": "WAV file I/O",
        "librosa": "Audio analysis",
        "numpy": "Numerical computing",
        "sklearn": "Machine learning",
        "pyttsx3": "Text-to-speech",
        "vosk": "Speech recognition",
    }
    
    all_ok = True
    
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {package:15} - {description}")
        except ImportError:
            print(f"✗ {package:15} - {description} [MISSING]")
            all_ok = False
    
    if not all_ok:
        print("\n[INSTALL MISSING PACKAGES]")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def check_vosk_model():
    """Check if VOSK model is installed"""
    print_step(3, "Checking VOSK Speech Model")
    
    vosk_dir = Path("vosk_model")
    model_marker = vosk_dir / "mfcc.txt"
    
    if model_marker.exists():
        print(f"✓ VOSK model found at: {vosk_dir.absolute()}")
        return True
    else:
        print(f"✗ VOSK model NOT found")
        print(f"\n  Model location: {vosk_dir.absolute()}")
        print(f"\n  TO INSTALL VOSK MODEL:")
        print(f"  1. Download: vosk-model-en-us-0.42-gigaspeech.zip")
        print(f"     From: https://alphacephei.com/vosk/models")
        print(f"  2. Extract to: {vosk_dir.absolute()}")
        print(f"  3. Verify: {vosk_dir}/mfcc.txt exists")
        return False

def verify_directories():
    """Check that required directories exist"""
    print_step(4, "Verifying Directory Structure")
    
    required_dirs = [
        "database",
        "data/raw_audio",
        "data/processed_features",
        "models",
        "logs",
        "gui",
        "audio",
        "features",
        "ml",
        "commands",
        "response",
        "speech",
        "utils",
    ]
    
    all_ok = True
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✓ {dir_name}")
        else:
            print(f"✗ {dir_name}")
            all_ok = False
    
    return all_ok

def run_tests():
    """Run test suite to verify system"""
    print_step(5, "Running System Tests")
    
    print("Running 10-test comprehensive suite...")
    print("This may take 1-2 minutes...\n")
    
    try:
        result = subprocess.run([sys.executable, "test_suite.py"], 
                              capture_output=True, text=True, timeout=120)
        
        # Check if all tests passed
        if result.returncode == 0 and "10/10 tests passed" in result.stdout:
            print("✓ All tests passed!")
            print("\nTest Summary: 10/10 PASSED")
            return True
        else:
            print("✗ Some tests failed")
            print(result.stdout[-500:])  # Show last 500 chars
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Tests timed out (>120 seconds)")
        return False
    except Exception as e:
        print(f"✗ Error running tests: {str(e)}")
        return False

def verify_startup():
    """Verify application startup"""
    print_step(6, "Verifying Application Startup")
    
    print("Testing application initialization...\n")
    
    try:
        result = subprocess.run([sys.executable, "verify_startup.py"], 
                              capture_output=True, text=True, timeout=30)
        
        if "STARTUP VERIFICATION SUCCESSFUL" in result.stdout:
            print("✓ Application startup verified!")
            return True
        else:
            print("✗ Startup verification failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Startup verification timed out")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def summary(checks):
    """Print final summary"""
    print_header("SETUP SUMMARY")
    
    results = [
        ("Python Version Check", checks[0]),
        ("Dependencies Check", checks[1]),
        ("VOSK Model Check", checks[2]),
        ("Directory Structure", checks[3]),
        ("Test Suite", checks[4]),
        ("Startup Verification", checks[5]),
    ]
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nRESULT: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n[OK] System is ready! Run: python app.py")
    else:
        print("\n[WARN] Fix issues above before launching app.py")
    
    print("\n" + "="*70 + "\n")
    
    return passed == total

def main():
    """Run complete setup verification"""
    print_header("VOICE AUTHENTICATION SYSTEM - SETUP HELPER")
    
    print("This script will verify your system is correctly configured.")
    print("It checks Python version, dependencies, and runs tests.\n")
    
    checks = [
        check_python_version(),
        check_dependencies(),
        check_vosk_model(),
        verify_directories(),
        run_tests(),
        verify_startup(),
    ]
    
    success = summary(checks)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
