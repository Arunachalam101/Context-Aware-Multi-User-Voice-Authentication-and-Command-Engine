"""
Complete system diagnostic for Voice Authentication Engine.
Run this to check all components before using the application.
"""

import sys
from pathlib import Path

def check_database():
    """Check database connectivity and schema."""
    try:
        from database.db_connection import DatabaseConnection
        from utils.config import DATABASE_FILE
        
        db = DatabaseConnection(str(DATABASE_FILE))
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table'
        """)
        tables = {row[0] for row in cursor.fetchall()}
        
        required_tables = {'users', 'voice_features', 'command_logs'}
        missing_tables = required_tables - tables
        
        if missing_tables:
            print(f"✗ Database: Missing tables {missing_tables}")
            return False
        
        # Count data
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM voice_features")
        feature_count = cursor.fetchone()[0]
        
        print(f"[OK] Database: Connected ({user_count} users, {feature_count} features)")
        return True
    except Exception as e:
        print(f"✗ Database Error: {str(e)}")
        return False

def check_model():
    """Check if model files exist."""
    try:
        from utils.config import SPEAKER_MODEL_FILE, SCALER_FILE
        
        model_exists = SPEAKER_MODEL_FILE.exists()
        scaler_exists = SCALER_FILE.exists()
        
        if not model_exists:
            print(f"[WARNING] Model: Not trained yet (first user needs to train)")
            return True  # Not an error - model gets created on first use
        
        if not scaler_exists:
            print(f"[WARNING] Scaler: Not found (will be created on first use)")
            return True  # Not an error
        
        # Try to load
        from ml.model_loader import ModelLoader
        loader = ModelLoader()
        loader.load_model()
        loader.load_scaler()
        
        print(f"[OK] Model: Loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Model Error: {str(e)}")
        return False

def check_mfcc():
    """Check MFCC feature extraction."""
    try:
        from features.mfcc_extractor import MFCCExtractor
        from utils.config import SAMPLE_RATE, N_MFCC
        
        extractor = MFCCExtractor(
            n_mfcc=N_MFCC,
            sr=SAMPLE_RATE
        )
        print(f"[OK] MFCC: Ready ({N_MFCC} coefficients at {SAMPLE_RATE}Hz)")
        return True
    except Exception as e:
        print(f"✗ MFCC Error: {str(e)}")
        return False

def check_vosk():
    """Check VOSK speech recognition."""
    try:
        from vosk import Model, KaldiRecognizer
        from utils.config import VOSK_MODEL_DIR
        
        if not VOSK_MODEL_DIR.exists():
            print(f"✗ VOSK: Model not found at {VOSK_MODEL_DIR}")
            print(f"   Fix: Download from https://alphacephei.com/vosk/models")
            return False
        
        print("[LOADING] VOSK: Loading model (this may take 20-30 seconds)...")
        model = Model(str(VOSK_MODEL_DIR))
        recognizer = KaldiRecognizer(model, 16000)
        
        print(f"[OK] VOSK: Model loaded and ready")
        return True
    except Exception as e:
        print(f"✗ VOSK Error: {str(e)}")
        return False

def check_tts():
    """Check text-to-speech engine."""
    try:
        from response.tts_engine import TextToSpeechEngine
        
        tts = TextToSpeechEngine()
        print(f"[OK] TTS: Engine ready")
        return True
    except Exception as e:
        print(f"✗ TTS Error: {str(e)}")
        return False

def check_vosk_recognizer():
    """Check VOSK recognizer integration."""
    try:
        from speech.vosk_recognizer import VoskRecognizer
        
        print("[LOADING] Initializing VOSK recognizer (this may take 30 seconds)...")
        recognizer = VoskRecognizer()
        if recognizer.is_initialized:
            print(f"[OK] VOSK Recognizer: Initialized")
            return True
        else:
            print(f"✗ VOSK Recognizer: Not initialized")
            return False
    except Exception as e:
        print(f"✗ VOSK Recognizer Error: {str(e)}")
        return False

def check_commands():
    """Check command configuration."""
    try:
        from utils.config import COMMANDS
        
        if not COMMANDS:
            print(f"✗ Commands: No commands defined")
            return False
        
        print(f"[OK] Commands: {len(COMMANDS)} defined")
        return True
    except Exception as e:
        print(f"✗ Commands Error: {str(e)}")
        return False

def check_audio_devices():
    """Check audio input/output devices."""
    try:
        import sounddevice as sd
        
        devices = sd.query_devices()
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        output_devices = [d for d in devices if d['max_output_channels'] > 0]
        
        if not input_devices:
            print(f"✗ Audio: No input device found")
            return False
        
        if not output_devices:
            print(f"✗ Audio: No output device found")
            return False
        
        print(f"[OK] Audio: {len(input_devices)} input, {len(output_devices)} output")
        return True
    except Exception as e:
        print(f"✗ Audio Error: {str(e)}")
        return False

def main():
    """Run all diagnostics."""
    print("\n" + "="*70)
    print("VOICE AUTHENTICATION SYSTEM - COMPLETE DIAGNOSTIC")
    print("="*70 + "\n")
    
    results = {
        "Database": check_database(),
        "Audio Devices": check_audio_devices(),
        "MFCC Extractor": check_mfcc(),
        "TTS Engine": check_tts(),
        "Commands": check_commands(),
        "Model": check_model(),
        "VOSK": check_vosk(),
        "VOSK Recognizer": check_vosk_recognizer(),
    }
    
    print("\n" + "="*70)
    print("📊 SUMMARY:")
    print("="*70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for component, status in results.items():
        status_str = "[OK]" if status else "[ERROR]"
        print(f"{status_str} {component}")
    
    print("\n" + "="*70)
    print(f"Result: {passed}/{total} components working")
    
    if passed == total:
        print("\n[SUCCESS] All systems operational!")
        print("   You can now run: python app.py")
        return 0
    else:
        print("\n[WARNING] Some components need attention. See errors above.")
        print("\nCommon fixes:")
        print("  1. VOSK model: Download from https://alphacephei.com/vosk/models")
        print("  2. Model not trained: Register first user and train model")
        print("  3. Audio devices: Check microphone and speaker connections")
        return 1

if __name__ == "__main__":
    sys.exit(main())
