"""
Audio utilities module for Voice Authentication Engine.

Provides helper functions for audio processing including:
- Audio normalization
- Silence detection
- Audio visualization
- Format conversion
"""

import numpy as np
import librosa
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# Import configuration
try:
    from utils.config import SAMPLE_RATE
except ImportError:
    SAMPLE_RATE = 16000


class AudioUtilError(Exception):
    """Raised when audio utility operations fail."""

    pass


def load_audio(filepath, sr=SAMPLE_RATE):
    """
    Load audio file using librosa.

    Args:
        filepath (str or Path): Path to audio file (WAV, MP3, etc).
        sr (int): Sample rate to resample to. Default: 16000

    Returns:
        tuple: (audio_data, sample_rate) as numpy array and int

    Raises:
        AudioUtilError: If file loading fails.
    """
    try:
        filepath = Path(filepath)
        if not filepath.exists():
            raise AudioUtilError(f"Audio file not found: {filepath}")

        audio, sr = librosa.load(str(filepath), sr=sr, mono=True)
        return audio, sr

    except Exception as e:
        raise AudioUtilError(f"Failed to load audio: {str(e)}")


def save_audio(audio, filepath, sr=SAMPLE_RATE):
    """
    Save audio array to file using librosa.

    Args:
        audio (np.ndarray): Audio data as numpy array.
        filepath (str or Path): Output file path.
        sr (int): Sample rate. Default: 16000

    Returns:
        Path: Path to saved file.

    Raises:
        AudioUtilError: If saving fails.
    """
    try:
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        librosa.output.write_wav(str(filepath), audio, sr)
        return filepath

    except Exception as e:
        raise AudioUtilError(f"Failed to save audio: {str(e)}")


def normalize_audio(audio, method="minmax"):
    """
    Normalize audio data.

    Args:
        audio (np.ndarray): Audio data.
        method (str): Normalization method ('minmax' or 'standard').

    Returns:
        np.ndarray: Normalized audio.
    """
    try:
        if method == "minmax":
            # Min-Max normalization: [0, 1]
            audio_min = np.min(audio)
            audio_max = np.max(audio)
            if audio_max - audio_min == 0:
                return np.zeros_like(audio)
            return (audio - audio_min) / (audio_max - audio_min)

        elif method == "standard":
            # StandardScaler: mean=0, std=1
            audio_mean = np.mean(audio)
            audio_std = np.std(audio)
            if audio_std == 0:
                return audio - audio_mean
            return (audio - audio_mean) / audio_std

        else:
            raise AudioUtilError(f"Unknown normalization method: {method}")

    except Exception as e:
        raise AudioUtilError(f"Normalization failed: {str(e)}")


def detect_silence(audio, threshold=0.02, sr=SAMPLE_RATE, frame_length=2048):
    """
    Detect silent regions in audio using energy threshold.

    Args:
        audio (np.ndarray): Audio data.
        threshold (float): Energy threshold for silence detection (0-1).
        sr (int): Sample rate.
        frame_length (int): Frame length for analysis.

    Returns:
        np.ndarray: Boolean array indicating silent frames.
    """
    try:
        # Calculate energy per frame
        S = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=frame_length)
        energy = np.sqrt(np.sum(S ** 2, axis=0))

        # Normalize energy
        energy_normalized = energy / np.max(energy)

        # Return silent frames
        return energy_normalized < threshold

    except Exception as e:
        raise AudioUtilError(f"Silence detection failed: {str(e)}")


def trim_silence(audio, top_db=40, sr=SAMPLE_RATE):
    """
    Trim silence from beginning and end of audio.

    Args:
        audio (np.ndarray): Audio data.
        top_db (float): Threshold in dB below reference to consider silence.
        sr (int): Sample rate.

    Returns:
        np.ndarray: Trimmed audio.
    """
    try:
        trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
        return trimmed

    except Exception as e:
        raise AudioUtilError(f"Failed to trim silence: {str(e)}")


def resample_audio(audio, orig_sr, target_sr):
    """
    Resample audio to different sample rate.

    Args:
        audio (np.ndarray): Audio data.
        orig_sr (int): Original sample rate.
        target_sr (int): Target sample rate.

    Returns:
        np.ndarray: Resampled audio.
    """
    try:
        if orig_sr == target_sr:
            return audio

        resampled = librosa.resample(audio, orig_sr=orig_sr, target_sr=target_sr)
        return resampled

    except Exception as e:
        raise AudioUtilError(f"Resampling failed: {str(e)}")


def get_audio_info(audio, sr=SAMPLE_RATE):
    """
    Get information about audio data.

    Args:
        audio (np.ndarray): Audio data.
        sr (int): Sample rate.

    Returns:
        dict: Dictionary with audio information.
    """
    try:
        return {
            "shape": audio.shape,
            "num_samples": len(audio),
            "duration_seconds": len(audio) / sr,
            "duration_ms": (len(audio) / sr) * 1000,
            "min_value": np.min(audio),
            "max_value": np.max(audio),
            "mean_value": np.mean(audio),
            "std_value": np.std(audio),
            "rms_energy": np.sqrt(np.mean(audio ** 2)),
        }

    except Exception as e:
        raise AudioUtilError(f"Failed to get audio info: {str(e)}")


def apply_preemphasis(audio, coef=0.97):
    """
    Apply preemphasis filter to audio.

    Emphasizes higher frequencies.

    Args:
        audio (np.ndarray): Audio data.
        coef (float): Preemphasis coefficient (0-1).

    Returns:
        np.ndarray: Preemphasized audio.
    """
    try:
        emphasized = np.append(
            audio[0], audio[1:] - coef * audio[:-1]
        )
        return emphasized

    except Exception as e:
        raise AudioUtilError(f"Preemphasis failed: {str(e)}")


def split_audio_into_frames(audio, frame_length=2048, hop_length=512):
    """
    Split audio into overlapping frames for analysis.

    Args:
        audio (np.ndarray): Audio data.
        frame_length (int): Length of each frame.
        hop_length (int): Number of samples between frames.

    Returns:
        np.ndarray: 2D array of frames (n_frames, frame_length).
    """
    try:
        frames = librosa.util.frame(audio, frame_length=frame_length, hop_length=hop_length)
        return frames.T

    except Exception as e:
        raise AudioUtilError(f"Frame splitting failed: {str(e)}")


def calculate_zero_crossing_rate(audio, frame_length=2048, hop_length=512):
    """
    Calculate zero-crossing rate of audio (indicator of voice activity).

    Args:
        audio (np.ndarray): Audio data.
        frame_length (int): Frame length.
        hop_length (int): Hop length.

    Returns:
        np.ndarray: Zero-crossing rate per frame.
    """
    try:
        zcr = librosa.feature.zero_crossing_rate(audio, frame_length=frame_length, hop_length=hop_length)
        return zcr[0]

    except Exception as e:
        raise AudioUtilError(f"ZCR calculation failed: {str(e)}")


def validate_audio(audio, min_duration=0.5, max_duration=10, sr=SAMPLE_RATE):
    """
    Validate audio quality and duration.

    Args:
        audio (np.ndarray): Audio data.
        min_duration (float): Minimum duration in seconds.
        max_duration (float): Maximum duration in seconds.
        sr (int): Sample rate.

    Returns:
        tuple: (is_valid, message)
    """
    try:
        duration = len(audio) / sr

        if duration < min_duration:
            return (
                False,
                f"Audio too short: {duration:.2f}s (minimum: {min_duration}s)"
            )

        if duration > max_duration:
            return (
                False,
                f"Audio too long: {duration:.2f}s (maximum: {max_duration}s)"
            )

        # Check for clipping
        if np.max(np.abs(audio)) > 0.99:
            return False, "Audio clipped detected (amplitude > 0.99)"

        # Check for sufficient variance
        if np.std(audio) < 0.001:
            return False, "Audio has insufficient variance (possibly silent)"

        return True, f"Audio valid: {duration:.2f}s, RMS: {np.sqrt(np.mean(audio**2)):.4f}"

    except Exception as e:
        return False, f"Validation error: {str(e)}"


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Audio Utilities - Test Mode")
    print("=" * 60 + "\n")

    # Create a test audio signal
    duration = 2
    frequency = 440  # A4 note
    sr = SAMPLE_RATE
    t = np.linspace(0, duration, sr * duration)
    test_audio = np.sin(2 * np.pi * frequency * t) * 0.3

    print(f"Created test audio: {frequency}Hz sine wave")
    info = get_audio_info(test_audio, sr)
    for key, value in info.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")

    print(f"\n✓ Audio utilities test completed!")
