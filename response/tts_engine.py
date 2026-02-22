"""
Text-to-Speech (TTS) response engine for voice authentication system.

Converts text responses to speech using pyttsx3 (completely offline).
"""

import pyttsx3
from pathlib import Path

# Import configuration
try:
    from utils.config import TTS_RATE, TTS_VOLUME, TTS_VOICE
except ImportError:
    TTS_RATE = 150
    TTS_VOLUME = 1.0
    TTS_VOICE = 0


class TTSError(Exception):
    """Raised when TTS operations fail."""

    pass


class TextToSpeechEngine:
    """
    Offline text-to-speech engine using pyttsx3.

    Provides methods to:
    - Initialize TTS engine
    - Speak text with configurable parameters
    - Get available voices
    - Set voice properties
    - Save speech to audio file
    """

    def __init__(self, rate=TTS_RATE, volume=TTS_VOLUME, voice_id=TTS_VOICE):
        """
        Initialize TTS engine.

        Args:
            rate (int): Speech rate in words per minute. Default: 150
            volume (float): Volume level (0.0 to 1.0). Default: 1.0
            voice_id (int): Voice index. Default: 0
        """
        try:
            self.engine = pyttsx3.init()
            self.rate = rate
            self.volume = volume
            self.voice_id = voice_id

            # Configure engine
            self.engine.setProperty("rate", rate)
            self.engine.setProperty("volume", volume)

            # Set voice
            self._set_voice(voice_id)

            print(f"[OK] TTS Engine initialized (rate={rate}wpm, volume={volume})")

        except Exception as e:
            raise TTSError(f"Failed to initialize TTS engine: {str(e)}")

    def _set_voice(self, voice_id):
        """
        Set the voice for TTS.

        Args:
            voice_id (int): Voice index.
        """
        try:
            voices = self.engine.getProperty("voices")

            if voice_id < len(voices):
                self.engine.setProperty("voice", voices[voice_id].id)
                self.current_voice = voices[voice_id].name
            else:
                print(f"⚠ Voice {voice_id} not found, using default")
                self.current_voice = voices[0].name if voices else "Default"

        except Exception as e:
            raise TTSError(f"Failed to set voice: {str(e)}")

    def get_available_voices(self):
        """
        Get list of available voices.

        Returns:
            list: List of voice name strings.
        """
        try:
            voices = self.engine.getProperty("voices")
            voice_names = [voice.name for voice in voices]
            return voice_names

        except Exception:
            return []

    def speak(self, text, wait=True):
        """
        Speak the given text.

        Args:
            text (str): Text to speak.
            wait (bool): Wait for speech to finish before returning.

        Raises:
            TTSError: If speech generation fails.
        """
        try:
            if not text:
                return

            print(f"🔊 Speaking: '{text}'")
            self.engine.say(text)

            if wait:
                self.engine.runAndWait()

        except Exception as e:
            raise TTSError(f"Failed to speak: {str(e)}")

    def speak_async(self, text):
        """
        Speak text asynchronously (non-blocking).

        Args:
            text (str): Text to speak.
        """
        try:
            if not text:
                return

            print(f"🔊 Speaking: '{text}' (async)")
            self.engine.say(text)
            # Don't wait for completion

        except Exception as e:
            raise TTSError(f"Async speech failed: {str(e)}")

    def save_to_file(self, text, filepath):
        """
        Save speech to audio file.

        Args:
            text (str): Text to speak.
            filepath (str or Path): Output file path (.mp3 or .wav).

        Returns:
            Path: Path to saved file.

        Raises:
            TTSError: If file saving fails.
        """
        try:
            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            self.engine.save_to_file(text, str(filepath))
            self.engine.runAndWait()

            print(f"✓ Audio saved: {filepath}")
            return filepath

        except Exception as e:
            raise TTSError(f"Failed to save audio: {str(e)}")

    def set_rate(self, rate):
        """
        Set speech rate.

        Args:
            rate (int): Speech rate in words per minute.
        """
        try:
            self.rate = rate
            self.engine.setProperty("rate", rate)
            print(f"✓ Speech rate set to {rate} wpm")

        except Exception as e:
            raise TTSError(f"Failed to set rate: {str(e)}")

    def set_volume(self, volume):
        """
        Set volume level.

        Args:
            volume (float): Volume level (0.0 to 1.0).
        """
        try:
            if not (0 <= volume <= 1.0):
                raise TTSError("Volume must be between 0 and 1")

            self.volume = volume
            self.engine.setProperty("volume", volume)
            print(f"✓ Volume set to {volume:.1%}")

        except Exception as e:
            raise TTSError(f"Failed to set volume: {str(e)}")

    def set_voice(self, voice_id):
        """
        Set voice by ID.

        Args:
            voice_id (int): Voice index.
        """
        try:
            self.voice_id = voice_id
            self._set_voice(voice_id)
            print(f"✓ Voice set to: {self.current_voice}")

        except Exception as e:
            raise TTSError(f"Failed to set voice: {str(e)}")

    def get_engine_info(self):
        """
        Get TTS engine information.

        Returns:
            dict: Engine configuration and capabilities.
        """
        return {
            "rate": self.rate,
            "volume": self.volume,
            "voice": self.current_voice if hasattr(self, "current_voice") else "Unknown",
            "available_voices": self.get_available_voices(),
            "engine": "pyttsx3",
        }

    def stop(self):
        """Stop current speech."""
        try:
            self.engine.stop()
            print("✓ Speech stopped")

        except Exception as e:
            raise TTSError(f"Failed to stop speech: {str(e)}")


class ResponseEngine:
    """
    High-level response engine that generates appropriate responses
    to user actions and speaks them.
    """

    def __init__(self):
        """Initialize response engine with TTS."""
        self.tts = TextToSpeechEngine()
        self.response_templates = {
            "authentication_success": "Welcome {username}. Authentication successful.",
            "authentication_failed": "Authentication failed. Please try again.",
            "command_executed": "Command executed successfully.",
            "command_failed": "Sorry, I could not execute that command.",
            "command_recognized": "I heard: {command}.",
            "command_unknown": "Sorry, I did not recognize that command.",
        }

    def speak_response(self, response_type, **kwargs):
        """
        Speak a predefined response.

        Args:
            response_type (str): Type of response (authentication_success, etc.)
            **kwargs: Template parameters.
        """
        try:
            template = self.response_templates.get(
                response_type,
                "Response"
            )
            message = template.format(**kwargs)
            self.tts.speak(message)

        except Exception as e:
            raise TTSError(f"Failed to speak response: {str(e)}")

    def speak_custom_message(self, message):
        """
        Speak a custom message.

        Args:
            message (str): Message to speak.
        """
        try:
            self.tts.speak(message)

        except Exception as e:
            raise TTSError(f"Failed to speak message: {str(e)}")

    def speak_authentication_result(self, authenticated, username=None):
        """
        Speak authentication result.

        Args:
            authenticated (bool): Whether authentication succeeded.
            username (str, optional): Authenticated username.
        """
        if authenticated:
            self.speak_response("authentication_success", username=username or "User")
        else:
            self.speak_response("authentication_failed")

    def speak_command_result(self, success, command=None):
        """
        Speak command execution result.

        Args:
            success (bool): Whether command succeeded.
            command (str, optional): Command name.
        """
        if success:
            self.speak_response("command_executed")
        else:
            self.speak_response("command_failed")


def speak_message(text):
    """
    Convenience function to speak a message.

    Args:
        text (str): Text to speak.

    Raises:
        TTSError: If speech fails.
    """
    try:
        tts = TextToSpeechEngine()
        tts.speak(text)

    except TTSError:
        raise


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Text-to-Speech Engine - Test Mode")
    print("=" * 70 + "\n")

    try:
        # Initialize TTS
        print("Initializing TTS engine...")
        tts = TextToSpeechEngine()

        print("\nEngine Information:")
        info = tts.get_engine_info()
        for key, value in info.items():
            if isinstance(value, list):
                print(f"  {key}: {len(value)} voices available")
            else:
                print(f"  {key}: {value}")

        print("\nAvailable Voices:")
        voices = tts.get_available_voices()
        for i, voice in enumerate(voices):
            print(f"  [{i}] {voice}")

        print("\n" + "-" * 70)
        print("Testing speech generation (muted in test):")
        print("-" * 70 + "\n")

        # Test TTS without actually playing (for testing)
        test_messages = [
            "Welcome to voice authentication system.",
            "Authentication successful.",
            "Command executed successfully.",
        ]

        for msg in test_messages:
            print(f"Message: '{msg}'")
            print("  (Would speak in real execution)\n")

        print("✓ TTS engine test completed!")

    except TTSError as e:
        print(f"✗ Test failed: {str(e)}")
