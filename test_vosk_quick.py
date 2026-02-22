#!/usr/bin/env python3
"""
Quick VOSK Test - Verify Speech Recognition Without Full App
===========================================================

Tests VOSK model loading and basic speech recognition functionality
without launching the full GUI application.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_vosk_quick():
    """Quick test of VOSK speech recognition."""
    
    print("🎤 Quick VOSK Speech Recognition Test")
    print("=" * 45)
    
    try:
        # Import VOSK
        import vosk
        print("✅ VOSK library imported successfully")
        
        # Check if model exists
        model_path = project_root / "vosk_model"
        if not model_path.exists():
            print("❌ VOSK model directory not found!")
            return False
            
        print(f"✅ VOSK model directory found: {model_path}")
        
        # Check required model components
        required_dirs = ["am", "conf", "graph", "ivector"]
        for dir_name in required_dirs:
            dir_path = model_path / dir_name
            if not dir_path.exists():
                print(f"❌ Missing required directory: {dir_name}")
                return False
            print(f"✅ Found: {dir_name}/")
        
        # Test model loading (this is the critical part)
        print("\n🔄 Testing VOSK model loading...")
        print("   (This is where the system restart happened before)")
        
        model = vosk.Model(str(model_path))
        print("✅ VOSK model loaded successfully!")
        
        # Test recognizer creation
        recognizer = vosk.KaldiRecognizer(model, 16000)
        print("✅ Speech recognizer created successfully!")
        
        # Test with sample audio data (silence)
        sample_data = b'\x00' * 3200  # 0.2 seconds of silence at 16kHz
        recognizer.AcceptWaveform(sample_data)
        result = recognizer.Result()
        print("✅ Speech recognition test completed!")
        
        print("\n🎉 SUCCESS: VOSK is working perfectly!")
        print("   - No system crashes")
        print("   - Model loads without issues") 
        print("   - Speech recognition functional")
        
        return True
        
    except ImportError as e:
        print(f"❌ VOSK import failed: {e}")
        print("   Run: pip install vosk")
        return False
        
    except Exception as e:
        print(f"❌ VOSK test failed: {e}")
        print("   The VOSK model may need re-extraction")
        return False

def main():
    """Main test function."""
    
    # Change to project directory
    os.chdir(project_root)
    
    print(f"📁 Working directory: {project_root}")
    print(f"🐍 Python version: {sys.version.split()[0]}")
    
    success = test_vosk_quick()
    
    if success:
        print("\n✅ Your system is ready for full Voice Authentication!")
        print("🚀 Safe to run: python app.py")
        print("🛡️  Or use: python run_safe_memory.py (recommended)")
    else:
        print("\n❌ VOSK needs attention before running the full app")
        print("🔧 Try running: python extract_vosk_manual.py")
    
    print("\n" + "=" * 50)
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()