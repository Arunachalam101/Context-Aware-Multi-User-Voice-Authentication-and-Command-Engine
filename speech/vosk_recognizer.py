"""
VOSK offline speech recognition module.

Converts speech to text using VOSK offline speech recognition engine.
No internet connection required.
"""

import json
import numpy as np
from pathlib import Path
import sys

# Import configuration
try:
    from utils.config import SAMPLE_RATE, VOSK_MODEL_DIR
except ImportError:
    SAMPLE_RATE = 16000
    VOSK_MODEL_DIR = Path("vosk_model")


class VoskRecognitionError(Exception):
    """Raised when speech recognition fails."""

    pass


class VoskRecognizer:
    """
    Offline speech recognition using VOSK.

    Provides methods to:
    - Initialize VOSK recognizer
    - Process audio frames
    - Extract recognized text
    - Handle partial and final results
    """

    def __init__(self, sample_rate=SAMPLE_RATE, model_path=None):
        """
        Initialize VOSK speech recognizer.

        Args:
            sample_rate (int): Audio sample rate.
            model_path (Path, optional): Path to VOSK model directory.

        Raises:
            VoskRecognitionError: If initialization fails.
        """
        self.sample_rate = sample_rate
        self.model_path = Path(model_path or VOSK_MODEL_DIR)
        self.recognizer = None
        self.is_initialized = False
        self.frame_size = int(sample_rate * 0.02)  # 20ms frames

        try:
            self._initialize_vosk()
        except Exception as e:
            raise VoskRecognitionError(f"Failed to initialize VOSK: {str(e)}")

    def _initialize_vosk(self):
        """Initialize VOSK recognizer."""
        try:
            from vosk import Model, KaldiRecognizer

            # Check if model exists
            if not self.model_path.exists():
                raise VoskRecognitionError(
                    f"VOSK model not found at {self.model_path}. "
                    "Download from https://alphacephei.com/vosk/models"
                )

            # Load model
            model = Model(str(self.model_path))
            self.recognizer = KaldiRecognizer(model, self.sample_rate)
            self.is_initialized = True

            print(f"✓ VOSK recognizer initialized (model: {self.model_path.name})")

        except ImportError:
            raise VoskRecognitionError(
                "vosk package not installed. Install with: pip install vosk"
            )
        except Exception as e:
            raise VoskRecognitionError(f"Initialization error: {str(e)}")

    def accept_waveform(self, audio_chunk):
        """
        Process audio chunk and check if word boundary detected.

        Args:
            audio_chunk (np.ndarray): Audio chunk (mono, float32).

        Returns:
            bool: True if word boundary detected, False otherwise.
        """
        if not self.is_initialized:
            raise VoskRecognitionError("Recognizer not initialized")

        try:
            # Convert float32 to int16 (scale to int16 range)
            audio_scaled = (audio_chunk * 32767).astype(np.int16)
            audio_bytes = audio_scaled.tobytes()
            return self.recognizer.AcceptWaveform(audio_bytes)

        except Exception as e:
            raise VoskRecognitionError(f"Error processing audio: {str(e)}")

    def get_partial_result(self):
        """
        Get partial recognition result (what's being said).

        Returns:
            str: Partial recognition text.
        """
        if not self.is_initialized:
            return ""

        try:
            result_json = json.loads(self.recognizer.PartialResult())
            return result_json.get("result", [])

        except Exception:
            return []

    def get_final_result(self):
        """
        Get final recognition result (completed word/sentence).

        Returns:
            str: Final recognition text.
        """
        if not self.is_initialized:
            return ""

        try:
            result_json = json.loads(self.recognizer.Result())
            
            # Handle both VOSK result formats:
            # Format 1: {'text': 'word'} - simple text format (newer VOSK)
            # Format 2: {'result': [{'result': 'word', 'conf': 0.95}]} - array format (older VOSK)
            
            # Try 'text' field first (common in recent VOSK versions)
            if "text" in result_json and result_json["text"]:
                return result_json["text"]
            
            # Fall back to 'result' field (array format)
            result_array = result_json.get("result", [])
            if isinstance(result_array, list):
                words = []
                for item in result_array:
                    if isinstance(item, dict) and "result" in item:
                        words.append(item["result"])
                    elif isinstance(item, str):
                        words.append(item)
                return " ".join(words) if words else ""
            
            return str(result_json.get("result", ""))

        except Exception:
            return ""

    def recognize_audio(self, audio):
        """
        Recognize speech from complete audio signal.

        Args:
            audio (np.ndarray): Audio data (mono, float32).

        Returns:
            str: Recognized text.

        Raises:
            VoskRecognitionError: If recognition fails.
        """
        if not self.is_initialized:
            raise VoskRecognitionError("Recognizer not initialized")

        try:
            # Reset recognizer for new audio
            from vosk import Model, KaldiRecognizer
            model = Model(str(self.model_path))
            recognizer = KaldiRecognizer(model, self.sample_rate)

            print(f"[DEBUG] Audio shape: {audio.shape}, dtype: {audio.dtype}")
            print(f"[DEBUG] Audio min: {np.min(audio):.4f}, max: {np.max(np.abs(audio)):.4f}")
            
            # Normalize audio if needed
            max_val = np.max(np.abs(audio))
            if max_val > 1.0:
                audio = audio / max_val
                print(f"[DEBUG] Normalized audio (was above 1.0)")
            
            # Ensure audio is not too quiet
            if max_val < 0.01:
                print(f"[WARNING] Audio is very quiet (max: {max_val:.4f})")

            # Process audio in frames
            frame_size = int(self.sample_rate * 0.02)  # 20ms frames
            final_text = ""
            partial_results = []

            print(f"[DEBUG] Processing audio with frame size: {frame_size}")

            for i in range(0, len(audio), frame_size):
                frame = audio[i:i + frame_size]

                if len(frame) < frame_size:
                    # Pad last frame
                    frame = np.pad(frame, (0, frame_size - len(frame)), mode='constant')

                # Convert to int16 (scale to int16 range)
                audio_bytes = (frame * 32767).astype(np.int16).tobytes()

                if recognizer.AcceptWaveform(audio_bytes):
                    # Got a final result
                    try:
                        result_json = json.loads(recognizer.Result())
                        print(f"[DEBUG] Got result: {result_json}")
                        print(f"[DEBUG] Result keys: {list(result_json.keys())}")
                        
                        # Handle both VOSK result formats:
                        # Format 1: {'text': 'word'} - simple text format
                        # Format 2: {'result': [{'result': 'word', 'conf': 0.95}]} - array format
                        
                        # Try 'text' field first (common in recent VOSK versions)
                        if "text" in result_json:
                            text_value = result_json["text"]
                            print(f"[DEBUG] Text value: {repr(text_value)}")
                            if text_value:  # Check if not empty
                                final_text = str(text_value)
                                print(f"[DEBUG] Got text field: {final_text}")
                        
                        if not final_text:
                            # Fall back to 'result' field (array format)
                            result_text = result_json.get("result", [])
                            print(f"[DEBUG] Trying result field: {result_text}")
                            if result_text:
                                if isinstance(result_text, list):
                                    # Extract words from result list
                                    words = []
                                    for item in result_text:
                                        if isinstance(item, dict):
                                            # Get the 'result' field which contains the actual word
                                            if "result" in item:
                                                words.append(item["result"])
                                        elif isinstance(item, str):
                                            words.append(item)
                                    if words:
                                        final_text = " ".join(words)
                                        print(f"[DEBUG] Extracted words: {final_text}")
                                else:
                                    # If result_text is a string, use it directly
                                    final_text = str(result_text)
                                    print(f"[DEBUG] Direct string result: {final_text}")
                    except Exception as e:
                        print(f"[ERROR] Error parsing result: {e}")
                        import traceback
                        traceback.print_exc()
                else:
                    # Get partial result
                    try:
                        partial = json.loads(recognizer.PartialResult())
                        partial_text = partial.get("partial", "")
                        if partial_text:
                            partial_results.append(partial_text)
                            print(f"[DEBUG] Partial: {partial_text}")
                    except:
                        pass

            # Get final result if no AcceptWaveform returned true
            if not final_text:
                try:
                    result_json = json.loads(recognizer.Result())
                    print(f"[DEBUG] Final fetch result: {result_json}")
                    print(f"[DEBUG] Result keys: {list(result_json.keys())}")
                    print(f"[DEBUG] Has 'text' key: {'text' in result_json}")
                    
                    # Handle both VOSK result formats:
                    # Format 1: {'text': 'word'} - simple text format
                    # Format 2: {'result': [{'result': 'word', 'conf': 0.95}]} - array format
                    
                    # Try 'text' field first (common in recent VOSK versions)
                    if "text" in result_json:
                        text_value = result_json["text"]
                        print(f"[DEBUG] Text value: {repr(text_value)}")
                        if text_value:  # Check if it's not empty
                            final_text = str(text_value)
                            print(f"[DEBUG] Got final text field: {final_text}")
                    
                    if not final_text:
                        # Fall back to 'result' field (array format)
                        result_text = result_json.get("result", [])
                        print(f"[DEBUG] Trying result field: {result_text}")
                        if result_text:
                            if isinstance(result_text, list):
                                words = []
                                for item in result_text:
                                    if isinstance(item, dict):
                                        if "result" in item:
                                            words.append(item["result"])
                                    elif isinstance(item, str):
                                        words.append(item)
                                if words:
                                    final_text = " ".join(words)
                                    print(f"[DEBUG] Final extracted words: {final_text}")
                            else:
                                final_text = str(result_text)
                                print(f"[DEBUG] Final direct result: {final_text}")
                except Exception as e:
                    print(f"[ERROR] Error fetching final result: {e}")

            print(f"[DEBUG] Final text result: '{final_text}'")
            return final_text.strip() if final_text else ""

        except Exception as e:
            print(f"[ERROR] Recognition exception: {e}")
            import traceback
            traceback.print_exc()
            raise VoskRecognitionError(f"Recognition failed: {str(e)}")

    def reset(self):
        """Reset recognizer for new recognition session."""
        try:
            if self.is_initialized:
                self._initialize_vosk()
                print("✓ Recognizer reset")
        except Exception as e:
            raise VoskRecognitionError(f"Reset failed: {str(e)}")


def recognize_speech(audio, model_path=None):
    """
    Convenience function for one-shot speech recognition.

    Args:
        audio (np.ndarray): Audio data.
        model_path (Path, optional): Path to VOSK model.

    Returns:
        str: Recognized text.

    Raises:
        VoskRecognitionError: If recognition fails.
    """
    try:
        recognizer = VoskRecognizer(model_path=model_path)
        return recognizer.recognize_audio(audio)

    except VoskRecognitionError:
        raise


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("VOSK Speech Recognizer - Test Mode")
    print("=" * 70 + "\n")

    try:
        # Check if VOSK model is available
        print("Checking for VOSK model...")
        if not VOSK_MODEL_DIR.exists():
            print(f"\n⚠ VOSK model not found at: {VOSK_MODEL_DIR}")
            print("\nTo use VOSK, download a model from:")
            print("https://alphacephei.com/vosk/models")
            print("\nAnd extract it to the vosk_model directory.")
            sys.exit(1)

        # Initialize recognizer
        print("Initializing VOSK recognizer...")
        recognizer = VoskRecognizer()

        # Create test audio (sine wave at 440Hz)
        duration = 2
        sr = SAMPLE_RATE
        t = np.linspace(0, duration, sr * duration)
        test_audio = np.sin(2 * np.pi * 440 * t) * 0.3

        print(f"Created test audio ({duration}s)")
        print("Recognizing speech...")

        text = recognizer.recognize_audio(test_audio)
        print(f"Recognized text: '{text}'")

        print("\n✓ Speech recognizer test completed!")

    except VoskRecognitionError as e:
        print(f"\n⚠ {str(e)}")
