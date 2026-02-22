"""
Microphone and speech recognition test tool.

Tests:
1. Microphone is working
2. Audio levels are good
3. VOSK is recognizing speech
4. Audio format is correct
"""

import sys
from pathlib import Path
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from audio.recorder import AudioRecorder, RecorderError
from utils.config import AUDIO_DURATION, SAMPLE_RATE
from speech.vosk_recognizer import VoskRecognizer, VoskRecognitionError


def test_microphone():
    """Test if microphone is working."""
    print("\n" + "=" * 70)
    print("TEST 1: MICROPHONE")
    print("=" * 70)
    
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        default_device = sd.default.device
        
        print(f"\n✓ Audio devices detected: {len(devices)}")
        print(f"✓ Default input device: {default_device}")
        print("\n🎤 Recording 2-second test audio...")
        
        recorder = AudioRecorder(duration=2)
        audio = recorder.record(show_progress=True)
        
        if audio is None:
            print("\n❌ Recording cancelled")
            return False
        
        # Check audio levels
        max_level = np.max(np.abs(audio))
        min_level = np.min(np.abs(audio))
        mean_level = np.mean(np.abs(audio))
        
        print(f"\n✓ Recording successful!")
        print(f"  Audio shape: {audio.shape}")
        print(f"  Sample rate: {SAMPLE_RATE} Hz")
        print(f"  Min level: {min_level:.4f}")
        print(f"  Max level: {max_level:.4f}")
        print(f"  Mean level: {mean_level:.4f}")
        
        # Check if audio is too quiet
        if max_level < 0.05:
            print(f"\n⚠️  WARNING: Audio is very quiet!")
            print(f"   Max level: {max_level:.4f}")
            print(f"   This might cause speech recognition to fail.")
            print(f"   Tips: Speak louder or move microphone closer")
            return False
        
        if max_level < 0.1:
            print(f"\n⚠️  Audio is quiet. Consider speaking louder.")
        
        if max_level > 1.0:
            print(f"\n⚠️  Audio is clipping/distorted (max > 1.0)")
            print(f"   Reduce microphone input level")
        
        print("\n✓ Microphone test PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Microphone test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_speech_recognition():
    """Test if speech recognition works."""
    print("\n" + "=" * 70)
    print("TEST 2: SPEECH RECOGNITION")
    print("=" * 70)
    
    try:
        print("\n🎤 Testing speech recognition...")
        print(f"   Please say a simple command like: 'openapp', 'playmusic', etc.")
        print(f"\n   Recording for {AUDIO_DURATION} seconds...")
        
        # Record audio
        recorder = AudioRecorder(duration=AUDIO_DURATION)
        audio = recorder.record(show_progress=True)
        
        if audio is None:
            print("\n❌ Recording cancelled")
            return False
        
        # Initialize VOSK
        print("\n⏳ Initializing VOSK speech recognizer...")
        print(f"   (This may take 10-20 seconds)...")
        
        recognizer = VoskRecognizer()
        
        # Recognize
        print("\n🔄 Processing audio...")
        recognized_text = recognizer.recognize_audio(audio)
        
        print(f"\n✓ Recognition complete!")
        print(f"   Recognized text: '{recognized_text}'")
        
        if not recognized_text or recognized_text.strip() == "":
            print(f"\n⚠️  No speech was recognized")
            print(f"   Try again with:")
            print(f"   • Clear speech")
            print(f"   • Louder voice")
            print(f"   • Simple command like 'openapp'")
            print(f"\n   Debug info:")
            print(f"     Audio shape: {audio.shape}")
            print(f"     Max level: {np.max(np.abs(audio)):.4f}")
            return False
        
        print("\n✓ Speech recognition test PASSED")
        return True
        
    except VoskRecognitionError as e:
        print(f"\n❌ VOSK error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Speech recognition test FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_tips():
    """Show tips for fixing speech recognition."""
    print("\n" + "=" * 70)
    print("TIPS FOR BETTER SPEECH RECOGNITION")
    print("=" * 70)
    
    print("\n💡 Microphone:")
    print("   • Ensure microphone is selected in Windows settings")
    print("   • Check microphone is not muted")
    print("   • Position microphone 6-12 inches from mouth")
    print("   • Close background applications (fans, music, etc.)")
    
    print("\n💡 Speech:")
    print("   • Speak clearly and naturally")
    print("   • Don't rush words")
    print("   • Use standard pronunciation")
    print("   • Speak at normal volume")
    
    print("\n💡 Commands:")
    print("   Common commands:")
    print("     • 'openapp'")
    print("     • 'closefile'")
    print("     • 'createdir'")
    print("     • 'playmusic'")
    print("     • 'checkstatus'")
    
    print("\n💡 Environment:")
    print("   • Test in quiet location")
    print("   • Close doors/windows to reduce noise")
    print("   • Stop other recordings/video calls")


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("🎤 MICROPHONE & SPEECH RECOGNITION TEST")
    print("=" * 70)
    
    # Test microphone
    mic_ok = test_microphone()
    
    if not mic_ok:
        print("\n❌ Microphone test failed. Cannot continue.")
        return 1
    
    # Test speech recognition
    speech_ok = test_speech_recognition()
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"\n  ✓ Microphone: {'PASS' if mic_ok else 'FAIL'}")
    print(f"  ✓ Speech Recognition: {'PASS' if speech_ok else 'FAIL'}")
    
    if mic_ok and speech_ok:
        print("\n✓ All tests passed! You're ready to use the application.")
        print("\nRun: python run_safe.py")
    else:
        print("\n❌ Some tests failed.")
        show_tips()
        print("\nTry testing again with the tips above.")
    
    print("=" * 70 + "\n")
    
    return 0 if (mic_ok and speech_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
