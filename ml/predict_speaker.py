"""
Speaker prediction module for voice authentication.

Uses trained model to authenticate speakers and predict speaker identity
from voice features.
"""

import numpy as np
from pathlib import Path
import sys

# Import ML modules
try:
    from ml.model_loader import ModelLoader, load_pretrained_model, ModelLoaderError
    from features.mfcc_extractor import MFCCExtractor, extract_features_from_audio, MFCCExtractionError
    from utils.config import AUTHENTICATION_THRESHOLD, SPEAKER_MODEL_FILE, SCALER_FILE
except ImportError:
    from .model_loader import ModelLoader, load_pretrained_model, ModelLoaderError
    from ..features.mfcc_extractor import MFCCExtractor, extract_features_from_audio, MFCCExtractionError
    from ..utils.config import AUTHENTICATION_THRESHOLD, SPEAKER_MODEL_FILE, SCALER_FILE


class PredictionError(Exception):
    """Raised when speaker prediction fails."""

    pass


class SpeakerAuthenticator:
    """
    Authenticates speakers using trained voice model.

    Provides methods to:
    - Load trained model
    - Extract features from audio
    - Predict speaker identity
    - Authenticate with confidence threshold
    - Get authentication results with metadata
    """

    def __init__(self, model_path=None, scaler_path=None):
        """
        Initialize speaker authenticator.

        Args:
            model_path (Path, optional): Path to trained model.
            scaler_path (Path, optional): Path to feature scaler.

        Raises:
            PredictionError: If model loading fails.
        """
        try:
            self.loader = load_pretrained_model(model_path, scaler_path)
            self.model = self.loader.model
            self.scaler = self.loader.scaler
            self.label_decoder = self.loader.label_decoder
            self.mfcc_extractor = None

        except ModelLoaderError as e:
            raise PredictionError(f"Failed to load model: {str(e)}")

    def process_audio(self, audio):
        """
        Extract MFCC features from audio.

        Args:
            audio (np.ndarray): Audio data.

        Returns:
            np.ndarray: Feature vector.

        Raises:
            PredictionError: If feature extraction fails.
        """
        try:
            if self.mfcc_extractor is None:
                self.mfcc_extractor = MFCCExtractor()

            features = self.mfcc_extractor.get_feature_vector(audio, compute_stats=True)
            return features

        except MFCCExtractionError as e:
            raise PredictionError(f"Feature extraction failed: {str(e)}")

    def predict_speaker(self, feature_vector, return_probabilities=False):
        """
        Predict speaker from feature vector.

        Args:
            feature_vector (np.ndarray): MFCC feature vector.
            return_probabilities (bool): Return probability for all speakers.

        Returns:
            dict: Prediction result with speaker, confidence, and metadata.
        """
        try:
            # Scale features
            feature_scaled = self.scaler.transform([feature_vector])

            # Get prediction and probabilities
            prediction = self.model.predict(feature_scaled)[0]
            probabilities = self.model.predict_proba(feature_scaled)[0]

            # Get speaker name
            predicted_speaker = self.label_decoder[prediction]
            confidence = float(probabilities[prediction])

            result = {
                "speaker": predicted_speaker,
                "confidence": confidence,
                "prediction_id": int(prediction),
            }

            if return_probabilities:
                prob_dict = {
                    self.label_decoder[i]: float(prob)
                    for i, prob in enumerate(probabilities)
                }
                result["all_probabilities"] = prob_dict

            return result

        except Exception as e:
            raise PredictionError(f"Speaker prediction failed: {str(e)}")

    def authenticate(self, feature_vector, threshold=None, return_details=False):
        """
        Authenticate speaker with confidence threshold.

        Returns "Unknown" if confidence is below threshold.

        Args:
            feature_vector (np.ndarray): MFCC feature vector.
            threshold (float, optional): Confidence threshold. Uses config default if None.
            return_details (bool): Return detailed authentication info.

        Returns:
            dict: Authentication result.
        """
        try:
            if threshold is None:
                threshold = AUTHENTICATION_THRESHOLD

            # Get prediction
            prediction = self.predict_speaker(feature_vector, return_probabilities=True)

            # Check threshold
            is_authenticated = prediction["confidence"] >= threshold
            identified_speaker = prediction["speaker"] if is_authenticated else "Unknown"

            result = {
                "authenticated": is_authenticated,
                "speaker": identified_speaker,
                "confidence": prediction["confidence"],
                "threshold": threshold,
            }

            if return_details:
                result["prediction_details"] = prediction
                result["all_probabilities"] = prediction["all_probabilities"]

            return result

        except Exception as e:
            raise PredictionError(f"Authentication failed: {str(e)}")

    def authenticate_from_audio(self, audio, threshold=None, return_details=False):
        """
        Authenticate speaker directly from audio data.

        High-level method combining feature extraction and authentication.

        Args:
            audio (np.ndarray): Audio data.
            threshold (float, optional): Confidence threshold.
            return_details (bool): Return detailed info.

        Returns:
            dict: Authentication result.

        Raises:
            PredictionError: If processing fails.
        """
        try:
            # Extract features
            features = self.process_audio(audio)

            # Authenticate
            result = self.authenticate(features, threshold, return_details)

            return result

        except Exception as e:
            raise PredictionError(f"Audio authentication failed: {str(e)}")

    def get_known_speakers(self):
        """
        Get list of speakers the model knows.

        Returns:
            list: List of known speaker names.
        """
        return list(self.label_decoder.values())

    def get_authenticator_info(self):
        """
        Get information about the authenticator.

        Returns:
            dict: Authenticator information.
        """
        return {
            "known_speakers": self.get_known_speakers(),
            "num_speakers": len(self.label_decoder),
            "authentication_threshold": AUTHENTICATION_THRESHOLD,
            "model_type": self.loader.metadata.get("model_type", "unknown"),
        }


def authenticate_voice(audio, model_path=None, threshold=None):
    """
    Convenience function for one-shot voice authentication.

    Args:
        audio (np.ndarray): Audio data.
        model_path (Path, optional): Path to trained model.
        threshold (float, optional): Confidence threshold.

    Returns:
        dict: Authentication result.

    Raises:
        PredictionError: If authentication fails.
    """
    try:
        authenticator = SpeakerAuthenticator(model_path)
        result = authenticator.authenticate_from_audio(audio, threshold)
        return result

    except PredictionError:
        raise


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Speaker Authenticator - Test Mode")
    print("=" * 70 + "\n")

    try:
        # Try to load model
        print("Attempting to load trained model...")
        authenticator = SpeakerAuthenticator()

        print("\nAuthenticator Information:")
        info = authenticator.get_authenticator_info()
        for key, value in info.items():
            print(f"  {key}: {value}")

        # Create synthetic test features
        print("\nCreating synthetic test features...")
        test_features = np.random.randn(26)

        print("Performing authentication...")
        result = authenticator.authenticate(test_features, return_details=True)

        print("\nAuthentication Result:")
        for key, value in result.items():
            if isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    if isinstance(v, float):
                        print(f"    {k}: {v:.4f}")
                    else:
                        print(f"    {k}: {v}")
            else:
                if isinstance(value, float):
                    print(f"  {key}: {value:.4f}")
                else:
                    print(f"  {key}: {value}")

        print("\n✓ Authenticator test completed!")

    except PredictionError as e:
        print(f"\n⚠ Note: {str(e)}")
        print("  Train a model first using train_model.py")
