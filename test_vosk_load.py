"""
VOSK Recognizer Load Test - Simulates AuthenticationWindow recognizer loading
"""

import sys
import threading
import time
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

print("=" * 70)
print("VOSK RECOGNIZER LOAD TEST")
print("=" * 70)

# Test 1: Check model path
print("\n[1] Checking VOSK model path...")
try:
    from utils.config import VOSK_MODEL_DIR
    print(f"    VOSK_MODEL_DIR = {VOSK_MODEL_DIR}")
    
    if not VOSK_MODEL_DIR.exists():
        print(f"    ❌ ERROR: Directory does not exist!")
        sys.exit(1)
    else:
        print(f"    ✓ Directory exists")
        
    # Check for required files
    required = ['am', 'conf', 'graph']
    for d in required:
        if not (VOSK_MODEL_DIR / d).exists():
            print(f"    ❌ ERROR: Missing required directory '{d}'")
            sys.exit(1)
    print(f"    ✓ All required directories present")
        
except Exception as e:
    print(f"    ❌ ERROR: {e}")
    sys.exit(1)

# Test 2: Import VOSK
print("\n[2] Importing VOSK...")
try:
    from vosk import Model, KaldiRecognizer
    print(f"    ✓ VOSK imported successfully")
except ImportError as e:
    print(f"    ❌ ERROR: {e}")
    sys.exit(1)

# Test 3: Load model (this takes 20-30 seconds)
print("\n[3] Loading VOSK model (this takes 20-30 seconds)...")
print(f"    Starting at: {time.strftime('%H:%M:%S')}")

start_time = time.time()
try:
    print(f"    Loading model from: {VOSK_MODEL_DIR}")
    model = Model(str(VOSK_MODEL_DIR))
    elapsed = time.time() - start_time
    print(f"    ✓ Model loaded in {elapsed:.1f} seconds")
    print(f"    Completed at: {time.strftime('%H:%M:%S')}")
except Exception as e:
    elapsed = time.time() - start_time
    print(f"    ❌ ERROR (after {elapsed:.1f}s): {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Create recognizer
print("\n[4] Creating KaldiRecognizer...")
try:
    from utils.config import SAMPLE_RATE
    recognizer = KaldiRecognizer(model, SAMPLE_RATE)
    print(f"    ✓ KaldiRecognizer created successfully")
except Exception as e:
    print(f"    ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Test with VoskRecognizer class
print("\n[5] Testing VoskRecognizer class...")
try:
    from speech.vosk_recognizer import VoskRecognizer
    print(f"    Creating VoskRecognizer...")
    vosk_rec = VoskRecognizer()
    print(f"    ✓ VoskRecognizer created successfully")
except Exception as e:
    print(f"    ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED - VOSK RECOGNIZER IS READY")
print("=" * 70)
print("\nThe speech recognizer should work in the application.")
print("If you still see 'Speech recognizer not ready' error:")
print("  1. Click on 'Record Voice for Authentication' first")
print("  2. Wait for authentication to complete")
print("  3. Then try 'Record Voice Command'")
print("  4. The app may still be loading VOSK in background (normal)")
