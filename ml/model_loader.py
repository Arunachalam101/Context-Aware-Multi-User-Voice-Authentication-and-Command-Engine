"""
Model loader module for speaker recognition.

Loads pre-trained models and scalers from disk and provides
inference capabilities.
"""

import pickle
import numpy as np
from pathlib import Path
import sys

# Import configuration
try:
    from utils.config import SPEAKER_MODEL_FILE, SCALER_FILE
except ImportError:
    SPEAKER_MODEL_FILE = Path("models/speaker_model.pkl")
    SCALER_FILE = Path("models/feature_scaler.pkl")


class ModelLoaderError(Exception):
    """Raised when model loading fails."""

    pass


class ModelLoader:
    """
    Loads and manages pre-trained speaker recognition models.

    Provides methods to:
    - Load model from disk
    - Load feature scaler
    - Verify model integrity
    - Get model information
    """

    def __init__(self, model_path=None, scaler_path=None):
        """
        Initialize model loader.

        Args:
            model_path (Path, optional): Path to model pickle file.
            scaler_path (Path, optional): Path to scaler pickle file.
        """
        self.model_path = Path(model_path or SPEAKER_MODEL_FILE)
        self.scaler_path = Path(scaler_path or SCALER_FILE)
        self.metadata_path = self.model_path.parent / "metadata.pkl"

        self.model = None
        self.scaler = None
        self.metadata = None
        self.label_decoder = None
        self.label_encoder = None

    def load_model(self):
        """
        Load the trained model from disk.

        Returns:
            object: Loaded model object.

        Raises:
            ModelLoaderError: If model loading fails.
        """
        try:
            if not self.model_path.exists():
                raise ModelLoaderError(f"Model file not found: {self.model_path}")

            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)

            print(f"✓ Model loaded: {self.model_path}")
            return self.model

        except Exception as e:
            raise ModelLoaderError(f"Failed to load model: {str(e)}")

    def load_scaler(self):
        """
        Load the feature scaler from disk.

        Returns:
            object: Loaded scaler object.

        Raises:
            ModelLoaderError: If scaler loading fails.
        """
        try:
            if not self.scaler_path.exists():
                raise ModelLoaderError(f"Scaler file not found: {self.scaler_path}")

            with open(self.scaler_path, "rb") as f:
                self.scaler = pickle.load(f)

            print(f"✓ Scaler loaded: {self.scaler_path}")
            return self.scaler

        except Exception as e:
            raise ModelLoaderError(f"Failed to load scaler: {str(e)}")

    def load_metadata(self):
        """
        Load model metadata (label encoders, model type, etc).

        Returns:
            dict: Metadata dictionary.

        Raises:
            ModelLoaderError: If metadata loading fails.
        """
        try:
            if not self.metadata_path.exists():
                raise ModelLoaderError(f"Metadata file not found: {self.metadata_path}")

            with open(self.metadata_path, "rb") as f:
                self.metadata = pickle.load(f)

            self.label_encoder = self.metadata.get("label_encoder", {})
            self.label_decoder = self.metadata.get("label_decoder", {})

            print(f"✓ Metadata loaded: {self.metadata_path}")
            return self.metadata

        except Exception as e:
            raise ModelLoaderError(f"Failed to load metadata: {str(e)}")

    def load_all(self):
        """
        Load model, scaler, and metadata in one call.

        Returns:
            tuple: (model, scaler, metadata)

        Raises:
            ModelLoaderError: If any loading step fails.
        """
        try:
            self.load_model()
            self.load_scaler()
            self.load_metadata()
            return self.model, self.scaler, self.metadata

        except ModelLoaderError:
            raise

    def verify_model_integrity(self):
        """
        Verify that all model files exist and are valid.

        Returns:
            tuple: (is_valid, message)
        """
        try:
            checks = {
                "Model file": self.model_path.exists(),
                "Scaler file": self.scaler_path.exists(),
                "Metadata file": self.metadata_path.exists(),
            }

            all_valid = all(checks.values())

            message = "All model files present" if all_valid else "Missing files:"
            for name, exists in checks.items():
                if not exists:
                    message += f"\n  - {name}: {name.lower()}"

            return all_valid, message

        except Exception as e:
            return False, f"Verification error: {str(e)}"

    def get_loaded_users(self):
        """
        Get list of users the model was trained on.

        Returns:
            list: List of usernames.
        """
        if self.label_decoder is None:
            return []
        return list(self.label_decoder.values())

    def get_model_info(self):
        """
        Get information about the loaded model.

        Returns:
            dict: Model information.
        """
        info = {
            "model_path": str(self.model_path),
            "scaler_path": str(self.scaler_path),
            "metadata_path": str(self.metadata_path),
            "model_type": self.metadata.get("model_type", "unknown") if self.metadata else "unknown",
            "num_speakers": len(self.label_decoder) if self.label_decoder else 0,
            "speakers": self.get_loaded_users(),
            "model_loaded": self.model is not None,
            "scaler_loaded": self.scaler is not None,
            "metadata_loaded": self.metadata is not None,
        }
        return info


def load_pretrained_model(model_path=None, scaler_path=None):
    """
    Convenience function to load model with all components.

    Args:
        model_path (Path, optional): Path to model file.
        scaler_path (Path, optional): Path to scaler file.

    Returns:
        ModelLoader: Loaded model loader object.

    Raises:
        ModelLoaderError: If loading fails.
    """
    try:
        loader = ModelLoader(model_path, scaler_path)
        loader.load_all()
        return loader

    except ModelLoaderError:
        raise


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Model Loader - Test Mode")
    print("=" * 70 + "\n")

    try:
        loader = ModelLoader()

        print("Verifying model files...")
        is_valid, message = loader.verify_model_integrity()
        print(f"  {message}")

        if is_valid:
            print("\nLoading model components...")
            loader.load_all()

            print("\nModel Information:")
            info = loader.get_model_info()
            for key, value in info.items():
                print(f"  {key}: {value}")

            print("\n✓ Model loader test completed!")
        else:
            print("\n⚠ Model files not found. Train a model first.")

    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}", file=sys.stderr)
