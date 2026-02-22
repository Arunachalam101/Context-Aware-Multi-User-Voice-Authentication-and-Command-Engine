"""
MFCC (Mel-Frequency Cepstral Coefficients) feature extraction module.

Extracts audio features suitable for speaker recognition and voice
authentication tasks using librosa library.
"""

import numpy as np
import librosa
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# Import configuration
try:
    from utils.config import (
        SAMPLE_RATE,
        N_MFCC,
        N_FFT,
        HOP_LENGTH,
        PROCESSED_FEATURES_DIR,
    )
except ImportError:
    SAMPLE_RATE = 16000
    N_MFCC = 13
    N_FFT = 2048
    HOP_LENGTH = 512
    PROCESSED_FEATURES_DIR = Path("data/processed_features")


class MFCCExtractionError(Exception):
    """Raised when MFCC extraction fails."""

    pass


class MFCCExtractor:
    """
    Extracts MFCC features from audio signals.

    Provides methods to:
    - Extract MFCC features from audio arrays
    - Load audio and extract features in one step
    - Compute statistical features from MFCCs
    - Save and load feature vectors
    """

    def __init__(
        self,
        n_mfcc=N_MFCC,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        sr=SAMPLE_RATE,
    ):
        """
        Initialize MFCC extractor.

        Args:
            n_mfcc (int): Number of MFCC coefficients. Default: 13
            n_fft (int): FFT window size. Default: 2048
            hop_length (int): Hop length for STFT. Default: 512
            sr (int): Sample rate. Default: 16000
        """
        self.n_mfcc = n_mfcc
        self.n_fft = n_fft
        self.hop_length = hop_length
        self.sr = sr
        self.mfcc_features = None
        self.mfcc_statistics = None

    def extract_mfcc(self, audio):
        """
        Extract MFCC features from audio data.

        Args:
            audio (np.ndarray): Audio data (1D array).

        Returns:
            np.ndarray: MFCC features (n_mfcc, time_steps).

        Raises:
            MFCCExtractionError: If extraction fails.
        """
        try:
            if len(audio.shape) != 1:
                raise MFCCExtractionError("Audio must be 1D array")

            # Extract MFCC features
            mfcc = librosa.feature.mfcc(
                y=audio,
                sr=self.sr,
                n_mfcc=self.n_mfcc,
                n_fft=self.n_fft,
                hop_length=self.hop_length,
            )

            self.mfcc_features = mfcc
            return mfcc

        except Exception as e:
            raise MFCCExtractionError(f"MFCC extraction failed: {str(e)}")

    def extract_from_file(self, filepath):
        """
        Load audio file and extract MFCC features.

        Args:
            filepath (str or Path): Path to audio file.

        Returns:
            np.ndarray: MFCC features.

        Raises:
            MFCCExtractionError: If file loading or extraction fails.
        """
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                raise MFCCExtractionError(f"File not found: {filepath}")

            # Load audio
            audio, _ = librosa.load(str(filepath), sr=self.sr, mono=True)

            # Extract MFCC
            return self.extract_mfcc(audio)

        except Exception as e:
            raise MFCCExtractionError(f"Failed to extract from file: {str(e)}")

    def compute_statistics(self, mfcc=None):
        """
        Compute statistical features from MFCC matrix.

        Computes mean and std for each MFCC coefficient, resulting in a
        feature vector of size (n_mfcc * 2).

        Args:
            mfcc (np.ndarray, optional): MFCC matrix. Uses last extracted if None.

        Returns:
            np.ndarray: Feature vector (n_mfcc * 2,).

        Raises:
            MFCCExtractionError: If computation fails.
        """
        try:
            if mfcc is None:
                if self.mfcc_features is None:
                    raise MFCCExtractionError("No MFCC data available")
                mfcc = self.mfcc_features

            # Compute mean and std for each coefficient
            mfcc_mean = np.mean(mfcc, axis=1)
            mfcc_std = np.std(mfcc, axis=1)

            # Concatenate into feature vector
            feature_vector = np.concatenate([mfcc_mean, mfcc_std])

            self.mfcc_statistics = feature_vector
            return feature_vector

        except Exception as e:
            raise MFCCExtractionError(f"Statistics computation failed: {str(e)}")

    def get_feature_vector(self, audio=None, compute_stats=True):
        """
        Extract and compute complete feature vector from audio.

        High-level method that extracts MFCC and optionally computes
        statistical features.

        Args:
            audio (np.ndarray, optional): Audio data. Extracts from array or
                                         uses last extracted if None.
            compute_stats (bool): Compute mean/std statistics. Default: True

        Returns:
            np.ndarray: Feature vector.

        Raises:
            MFCCExtractionError: If extraction fails.
        """
        try:
            # Extract MFCC if audio provided
            if audio is not None:
                mfcc = self.extract_mfcc(audio)
            else:
                if self.mfcc_features is None:
                    raise MFCCExtractionError("No audio data provided")
                mfcc = self.mfcc_features

            # Compute statistics if requested
            if compute_stats:
                return self.compute_statistics(mfcc)
            else:
                # Return flattened MFCC matrix
                return mfcc.flatten()

        except Exception as e:
            raise MFCCExtractionError(f"Feature vector computation failed: {str(e)}")

    def save_features(self, filepath, feature_vector=None):
        """
        Save feature vector to file (numpy binary format).

        Args:
            filepath (str or Path): Output file path.
            feature_vector (np.ndarray, optional): Feature vector to save.
                                                   Uses last computed if None.

        Returns:
            Path: Path to saved file.

        Raises:
            MFCCExtractionError: If saving fails.
        """
        try:
            if feature_vector is None:
                if self.mfcc_statistics is None:
                    raise MFCCExtractionError("No feature vector to save")
                feature_vector = self.mfcc_statistics

            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            np.save(str(filepath), feature_vector)
            print(f"✓ Features saved: {filepath}")
            return filepath

        except Exception as e:
            raise MFCCExtractionError(f"Failed to save features: {str(e)}")

    def load_features(self, filepath):
        """
        Load feature vector from file.

        Args:
            filepath (str or Path): Path to feature file (.npy).

        Returns:
            np.ndarray: Loaded feature vector.

        Raises:
            MFCCExtractionError: If loading fails.
        """
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                raise MFCCExtractionError(f"Feature file not found: {filepath}")

            feature_vector = np.load(str(filepath))
            self.mfcc_statistics = feature_vector
            return feature_vector

        except Exception as e:
            raise MFCCExtractionError(f"Failed to load features: {str(e)}")

    def get_mfcc_info(self):
        """
        Get information about extracted MFCC features.

        Returns:
            dict: Dictionary with MFCC information.
        """
        if self.mfcc_features is None:
            return {"status": "No MFCC data extracted yet"}

        return {
            "n_mfcc": self.n_mfcc,
            "n_coefficients": self.mfcc_features.shape[0],
            "n_time_steps": self.mfcc_features.shape[1],
            "shape": self.mfcc_features.shape,
            "min_value": np.min(self.mfcc_features),
            "max_value": np.max(self.mfcc_features),
            "mean_value": np.mean(self.mfcc_features),
            "std_value": np.std(self.mfcc_features),
        }

    def get_statistics_info(self):
        """
        Get information about computed statistics.

        Returns:
            dict: Dictionary with statistics information.
        """
        if self.mfcc_statistics is None:
            return {"status": "No statistics computed yet"}

        return {
            "feature_vector_size": len(self.mfcc_statistics),
            "n_mfcc": self.n_mfcc,
            "n_means": self.n_mfcc,
            "n_stds": self.n_mfcc,
            "min_value": np.min(self.mfcc_statistics),
            "max_value": np.max(self.mfcc_statistics),
            "mean_value": np.mean(self.mfcc_statistics),
            "std_value": np.std(self.mfcc_statistics),
        }


def extract_features_from_file(filepath, n_mfcc=N_MFCC, compute_stats=True):
    """
    Convenience function to extract features from audio file in one call.

    Args:
        filepath (str or Path): Path to audio file.
        n_mfcc (int): Number of MFCC coefficients.
        compute_stats (bool): Compute mean/std statistics.

    Returns:
        np.ndarray: Feature vector.

    Raises:
        MFCCExtractionError: If extraction fails.
    """
    try:
        extractor = MFCCExtractor(n_mfcc=n_mfcc)
        mfcc = extractor.extract_from_file(filepath)

        if compute_stats:
            return extractor.compute_statistics(mfcc)
        else:
            return mfcc.flatten()

    except Exception as e:
        raise MFCCExtractionError(f"Feature extraction failed: {str(e)}")


def extract_features_from_audio(audio, sr=SAMPLE_RATE, n_mfcc=N_MFCC, compute_stats=True):
    """
    Convenience function to extract features from audio array in one call.

    Args:
        audio (np.ndarray): Audio data.
        sr (int): Sample rate.
        n_mfcc (int): Number of MFCC coefficients.
        compute_stats (bool): Compute mean/std statistics.

    Returns:
        np.ndarray: Feature vector.

    Raises:
        MFCCExtractionError: If extraction fails.
    """
    try:
        extractor = MFCCExtractor(n_mfcc=n_mfcc, sr=sr)
        return extractor.get_feature_vector(audio, compute_stats=compute_stats)

    except Exception as e:
        raise MFCCExtractionError(f"Feature extraction failed: {str(e)}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("MFCC Extractor - Test Mode")
    print("=" * 70 + "\n")

    # Create test audio signal
    duration = 2
    frequency = 440  # A4 note
    sr = SAMPLE_RATE
    t = np.linspace(0, duration, sr * duration)
    test_audio = np.sin(2 * np.pi * frequency * t) * 0.3

    print(f"Created test audio: {frequency}Hz sine wave")
    print(f"Audio shape: {test_audio.shape}")
    print(f"Duration: {duration}s\n")

    # Extract MFCC
    extractor = MFCCExtractor(n_mfcc=13)

    print("Extracting MFCC features...")
    mfcc = extractor.extract_mfcc(test_audio)
    print(f"✓ MFCC shape: {mfcc.shape}\n")

    print("MFCC Information:")
    info = extractor.get_mfcc_info()
    for key, value in info.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")

    print("\nComputing statistics...")
    feature_vector = extractor.compute_statistics()
    print(f"✓ Feature vector size: {len(feature_vector)}\n")

    print("Feature Vector Statistics:")
    info = extractor.get_statistics_info()
    for key, value in info.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.4f}")
        else:
            print(f"  {key}: {value}")

    print(f"\n✓ MFCC extraction test completed!")
