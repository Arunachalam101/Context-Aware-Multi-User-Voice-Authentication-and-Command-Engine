"""
Audio recording module for Voice Authentication Engine.

Provides functionality to record audio samples from microphone
using sounddevice library. Handles audio capture for both
user registration and voice authentication.
"""

import sounddevice as sd
import soundfile as sf
import numpy as np
from pathlib import Path
import sys
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Import configuration
try:
    from utils.config import (
        SAMPLE_RATE,
        AUDIO_DURATION,
        CHANNELS,
        DTYPE,
        RAW_AUDIO_DIR,
    )
except ImportError:
    # Fallback if import fails
    SAMPLE_RATE = 16000
    AUDIO_DURATION = 3
    CHANNELS = 1
    DTYPE = "float32"
    RAW_AUDIO_DIR = Path("data/raw_audio")


class RecorderError(Exception):
    """Raised when recording fails."""

    pass


class AudioRecorder:
    """
    Handles audio recording from microphone.

    Provides methods to:
    - Record audio samples with visual feedback
    - Save recordings to WAV files
    - Validate audio quality
    - Handle microphone errors
    """

    def __init__(
        self,
        sample_rate=SAMPLE_RATE,
        duration=AUDIO_DURATION,
        channels=CHANNELS,
        dtype=DTYPE,
    ):
        """
        Initialize the audio recorder.

        Args:
            sample_rate (int): Sample rate in Hz. Default: 16000
            duration (float): Duration of recording in seconds. Default: 3
            channels (int): Number of channels (1=mono, 2=stereo). Default: 1
            dtype (str): Audio data type. Default: 'float32'

        Raises:
            RecorderError: If device initialization fails.
        """
        self.sample_rate = sample_rate
        self.duration = duration
        self.channels = channels
        self.dtype = dtype
        self.audio_data = None

        # Verify audio device is available
        try:
            devices = sd.query_devices()
            if len(devices) == 0:
                raise RecorderError("No audio input device detected")
            print(f"✓ Audio device detected: {sd.default.device}")
        except Exception as e:
            raise RecorderError(f"Failed to initialize audio device: {str(e)}")

    def record(self, show_progress=True):
        """
        Record audio from microphone.

        Args:
            show_progress (bool): Show recording progress. Default: True

        Returns:
            np.ndarray: Recorded audio data as numpy array.

        Raises:
            RecorderError: If recording fails.
        """
        try:
            if show_progress:
                print(
                    f"\n🎤 Recording for {self.duration} seconds... Press Ctrl+C to cancel"
                )

            # Record audio
            self.audio_data = sd.rec(
                int(self.sample_rate * self.duration),
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=self.dtype,
                blocksize=4410,  # 250ms blocks for visual feedback
            )

            # Wait for recording to complete with progress indication
            import time
            frames_recorded = 0
            total_frames = int(self.sample_rate * self.duration)
            start_time = time.time()

            while frames_recorded < total_frames:
                time.sleep(0.25)  # Wait 250ms
                elapsed = time.time() - start_time
                frames_recorded = int(self.sample_rate * elapsed)
                if show_progress and frames_recorded < total_frames:
                    progress = int((frames_recorded / total_frames) * 20)
                    print(f"  {'█' * progress}{'░' * (20 - progress)} {min(frames_recorded, total_frames)}/{total_frames} frames",
                          end="\r")

            # Final wait to ensure all data is recorded
            sd.wait()

            # Squeeze to 1D if mono (remove channel dimension)
            if self.channels == 1:
                self.audio_data = np.squeeze(self.audio_data)

            if show_progress:
                print(f"\n✓ Recording complete! Audio shape: {self.audio_data.shape}")

            return self.audio_data

        except KeyboardInterrupt:
            print("\n⚠ Recording cancelled by user")
            self.audio_data = None
            raise RecorderError("Recording cancelled by user")
        except Exception as e:
            raise RecorderError(f"Recording failed: {str(e)}")

    def save_recording(self, filepath):
        """
        Save recorded audio to a WAV file.

        Args:
            filepath (str or Path): Path to save the WAV file.

        Returns:
            Path: Path to the saved file.

        Raises:
            RecorderError: If saving fails.
        """
        if self.audio_data is None:
            raise RecorderError("No audio recorded. Call record() first.")

        try:
            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Normalize audio to prevent clipping
            max_val = np.max(np.abs(self.audio_data))
            if max_val > 1.0:
                self.audio_data = self.audio_data / (max_val * 1.05)

            # Save to WAV file
            sf.write(str(filepath), self.audio_data, self.sample_rate)
            print(f"✓ Audio saved to: {filepath}")
            return filepath

        except Exception as e:
            raise RecorderError(f"Failed to save audio: {str(e)}")

    def get_audio_array(self):
        """
        Get the recorded audio data as numpy array.

        Returns:
            np.ndarray: Audio data or None if no recording.
        """
        return self.audio_data

    def get_duration_ms(self):
        """
        Get duration of recorded audio in milliseconds.

        Returns:
            float: Duration in milliseconds.
        """
        if self.audio_data is None:
            return 0
        return (len(self.audio_data) / self.sample_rate) * 1000

    def clear(self):
        """Clear the current audio data."""
        self.audio_data = None


def record_voice_sample(username, sample_number, duration=AUDIO_DURATION):
    """
    Record a voice sample for user registration.

    High-level function to record and save a voice sample.

    Args:
        username (str): Name of the user registering.
        sample_number (int): Sample number for this user (1, 2, 3, ...).
        duration (float): Duration of recording in seconds.

    Returns:
        Path: Path to the saved audio file.

    Raises:
        RecorderError: If recording or saving fails.
    """
    try:
        # Create output filepath
        audio_filename = f"{username}_sample_{sample_number}.wav"
        audio_filepath = RAW_AUDIO_DIR / username / audio_filename

        # Record audio
        recorder = AudioRecorder(duration=duration)
        print(f"\n{'='*60}")
        print(f"Recording sample {sample_number} for user: {username}")
        print(f"{'='*60}")

        recorder.record(show_progress=True)

        # Save recording
        filepath = recorder.save_recording(audio_filepath)
        print(f"✓ Sample {sample_number} saved successfully\n")

        return filepath

    except RecorderError as e:
        raise RecorderError(f"Failed to record voice sample: {str(e)}")


def get_microphone_devices():
    """
    Get list of available audio input devices.

    Returns:
        dict: Dictionary mapping device names to device IDs.
    """
    try:
        devices = sd.query_devices()
        input_devices = {}

        for i, device in enumerate(devices):
            if device["max_input_channels"] > 0:
                input_devices[device["name"]] = i

        return input_devices
    except Exception as e:
        print(f"⚠ Failed to query devices: {str(e)}")
        return {}


if __name__ == "__main__":
    # Test the recorder
    print("\n" + "=" * 60)
    print("Audio Recorder - Test Mode")
    print("=" * 60 + "\n")

    try:
        # List available devices
        print("Available audio input devices:")
        devices = get_microphone_devices()
        for name, device_id in devices.items():
            print(f"  [{device_id}] {name}")

        print()

        # Record a test sample
        recorder = AudioRecorder(duration=3)
        print("Recording 3-second test sample...")
        audio = recorder.record(show_progress=True)

        # Save it
        test_filepath = RAW_AUDIO_DIR / "test_recording.wav"
        recorder.save_recording(test_filepath)

        print(f"\n✓ Test completed successfully!")
        print(f"  Audio shape: {audio.shape}")
        print(f"  Duration: {recorder.get_duration_ms():.0f}ms")

    except RecorderError as e:
        print(f"\n✗ Test failed: {str(e)}", file=sys.stderr)
        sys.exit(1)
