"""
VOSK Setup Verification Script

Checks if VOSK and its model are properly installed.
Run this script to diagnose VOSK-related issues.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def check_vosk_installed():
    """Check if vosk package is installed."""
    try:
        import vosk
        print("✅ VOSK package is installed")
        print(f"   Version: {vosk.__version__ if hasattr(vosk, '__version__') else 'Unknown'}")
        return True
    except ImportError:
        print("❌ VOSK package is NOT installed")
        print("   Install with: pip install vosk")
        return False


def check_vosk_model():
    """Check if VOSK model is present."""
    from utils.config import VOSK_MODEL_DIR, VOSK_MODEL_NAME
    
    print(f"\n📁 Checking VOSK model location:")
    print(f"   Expected path: {VOSK_MODEL_DIR}")
    print(f"   Model name: {VOSK_MODEL_NAME}")
    
    if not VOSK_MODEL_DIR.exists():
        print(f"❌ VOSK model directory does NOT exist")
        print(f"   Please download from: https://alphacephei.com/vosk/models")
        print(f"   And extract to: {VOSK_MODEL_DIR.parent}")
        return False
    
    # Check if model files/directories exist
    required_dirs = ['am', 'conf', 'graph', 'ivector']
    found_dirs = [d for d in required_dirs if (VOSK_MODEL_DIR / d).exists()]
    
    if found_dirs:
        print(f"✅ VOSK model directory exists with required files")
        print(f"   Found directories: {', '.join(found_dirs)}")
        return True
    else:
        print(f"❌ VOSK model directory exists but missing required files")
        print(f"   Expected directories: {', '.join(required_dirs)}")
        print(f"   In: {VOSK_MODEL_DIR}")
        return False


def check_vosk_recognizer():
    """Check if VoskRecognizer can be initialized."""
    try:
        from speech.vosk_recognizer import VoskRecognizer
        print(f"\n🎤 Attempting to initialize VoskRecognizer...")
        
        recognizer = VoskRecognizer()
        print(f"✅ VoskRecognizer initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize VoskRecognizer")
        print(f"   Error: {str(e)}")
        return False


def main():
    """Run all checks."""
    print("=" * 60)
    print("VOSK SETUP VERIFICATION")
    print("=" * 60)
    
    vosk_installed = check_vosk_installed()
    vosk_model = check_vosk_model()
    recognizer_ok = False
    
    if vosk_installed and vosk_model:
        recognizer_ok = check_vosk_recognizer()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if vosk_installed and vosk_model and recognizer_ok:
        print("✅ All checks passed! VOSK is ready to use.")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        if not vosk_installed:
            print("\n1. Install VOSK:")
            print("   pip install vosk")
        if not vosk_model:
            print("\n2. Download VOSK model:")
            print("   - Go to https://alphacephei.com/vosk/models")
            print("   - Download 'vosk-model-en-us-0.42-gigaspeech'")
            print("   - Extract to: vosk_model/")
        return 1


if __name__ == "__main__":
    sys.exit(main())
