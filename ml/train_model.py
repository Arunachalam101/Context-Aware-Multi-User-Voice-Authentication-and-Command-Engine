"""
Machine learning model training module for speaker recognition.

Trains a classifier on voice feature vectors and saves the model.
Supports SVM and Random Forest algorithms.
"""

import numpy as np
import pickle
from pathlib import Path
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import warnings

warnings.filterwarnings("ignore")

# Import configuration and database
try:
    from utils.config import (
        MODEL_TYPE,
        SVM_KERNEL,
        SVM_C,
        SVM_GAMMA,
        RANDOM_FOREST_N_ESTIMATORS,
        RANDOM_FOREST_MAX_DEPTH,
        SPEAKER_MODEL_FILE,
        SCALER_FILE,
        MIN_SAMPLES_FOR_TRAINING,
    )
    from database.db_operations import VoiceFeatureManager
except ImportError:
    MODEL_TYPE = "svm"
    SVM_KERNEL = "rbf"
    SVM_C = 1.0
    SVM_GAMMA = "scale"
    RANDOM_FOREST_N_ESTIMATORS = 100
    RANDOM_FOREST_MAX_DEPTH = 10
    SPEAKER_MODEL_FILE = Path("models/speaker_model.pkl")
    SCALER_FILE = Path("models/feature_scaler.pkl")
    MIN_SAMPLES_FOR_TRAINING = 3


class ModelTrainingError(Exception):
    """Raised when model training fails."""

    pass


class SpeakerRecognitionModel:
    """
    Trains and manages speaker recognition model.

    Supports:
    - SVM classifier with RBF, linear, or polynomial kernels
    - Random Forest classifier
    - Feature scaling and normalization
    - Model persistence (save/load)
    """

    def __init__(self, model_type=MODEL_TYPE, **kwargs):
        """
        Initialize speaker recognition model.

        Args:
            model_type (str): 'svm' or 'random_forest'.
            **kwargs: Additional arguments for model configuration.
        """
        self.model_type = model_type.lower()
        self.model = None
        self.scaler = StandardScaler()
        self.feature_vectors = None
        self.labels = None
        self.label_encoder = {}  # Maps username to numeric label
        self.label_decoder = {}  # Maps numeric label to username
        self.is_trained = False

        if self.model_type == "svm":
            self._init_svm(**kwargs)
        elif self.model_type == "random_forest":
            self._init_random_forest(**kwargs)
        else:
            raise ModelTrainingError(f"Unknown model type: {model_type}")

    def _init_svm(self, kernel=SVM_KERNEL, C=SVM_C, gamma=SVM_GAMMA, **kwargs):
        """Initialize SVM model."""
        self.model = SVC(kernel=kernel, C=C, gamma=gamma, probability=True)
        print(f"[OK] SVM model initialized (kernel={kernel}, C={C}, gamma={gamma})")

    def _init_random_forest(self, n_estimators=RANDOM_FOREST_N_ESTIMATORS,
                           max_depth=RANDOM_FOREST_MAX_DEPTH, **kwargs):
        """Initialize Random Forest model."""
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42,
        )
        print(f"[OK] Random Forest model initialized (estimators={n_estimators}, depth={max_depth})")

    def prepare_training_data(self, feature_vectors, usernames):
        """
        Prepare and normalize training data.

        Args:
            feature_vectors (list): List of numpy arrays (features).
            usernames (list): List of corresponding usernames.

        Raises:
            ModelTrainingError: If data preparation fails.
        """
        try:
            if len(feature_vectors) != len(usernames):
                raise ModelTrainingError("Feature vectors and usernames length mismatch")

            if len(feature_vectors) < MIN_SAMPLES_FOR_TRAINING:
                raise ModelTrainingError(
                    f"Insufficient training data. Minimum {MIN_SAMPLES_FOR_TRAINING} "
                    f"samples required, got {len(feature_vectors)}"
                )

            # Convert to numpy array and normalize
            X = np.array(feature_vectors)
            print(f"[OK] Data shape: {X.shape}")

            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            print(f"[OK] Features scaled (mean=0, std=1)")

            # Create label encoding
            unique_users = sorted(set(usernames))
            self.label_encoder = {user: idx for idx, user in enumerate(unique_users)}
            self.label_decoder = {idx: user for user, idx in self.label_encoder.items()}

            y = np.array([self.label_encoder[user] for user in usernames])
            print(f"[OK] Labels encoded: {self.label_encoder}")

            self.feature_vectors = X_scaled
            self.labels = y

            return X_scaled, y

        except Exception as e:
            raise ModelTrainingError(f"Failed to prepare training data: {str(e)}")

    def train(self, feature_vectors=None, usernames=None):
        """
        Train the speaker recognition model.

        Args:
            feature_vectors (list, optional): Training feature vectors.
            usernames (list, optional): Corresponding usernames.
                                       If None, uses prepared data.

        Raises:
            ModelTrainingError: If training fails.
        """
        try:
            if feature_vectors is not None and usernames is not None:
                X_train, y_train = self.prepare_training_data(feature_vectors, usernames)
            else:
                if self.feature_vectors is None:
                    raise ModelTrainingError("No training data provided")
                X_train, y_train = self.feature_vectors, self.labels

            print(f"\n{'='*60}")
            print(f"Training {self.model_type.upper()} Model")
            print(f"{'='*60}")
            print(f"Training samples: {X_train.shape[0]}")
            print(f"Feature dimensions: {X_train.shape[1]}")
            print(f"Number of speakers: {len(self.label_decoder)}")

            # Train model
            self.model.fit(X_train, y_train)
            self.is_trained = True

            print(f"[OK] Model training completed!")

            # Print model info
            print(f"\nModel Configuration:")
            print(f"  Type: {self.model_type}")
            if self.model_type == "svm":
                print(f"  Kernel: {self.model.kernel}")
                print(f"  Support vectors: {len(self.model.support_vectors_)}")
            else:
                print(f"  Estimators: {self.model.n_estimators}")
                print(f"  Max depth: {self.model.max_depth}")

        except Exception as e:
            raise ModelTrainingError(f"Model training failed: {str(e)}")

    def predict(self, feature_vector):
        """
        Predict speaker for a single feature vector.

        Args:
            feature_vector (np.ndarray): Feature vector to predict.

        Returns:
            tuple: (username, confidence)

        Raises:
            ModelTrainingError: If model not trained or prediction fails.
        """
        try:
            if not self.is_trained:
                raise ModelTrainingError("Model not trained yet")

            # Scale the feature vector
            feature_scaled = self.scaler.transform([feature_vector])

            # Get prediction and probability
            prediction = self.model.predict(feature_scaled)[0]
            probabilities = self.model.predict_proba(feature_scaled)[0]

            username = self.label_decoder[prediction]
            confidence = float(np.max(probabilities))

            return username, confidence

        except Exception as e:
            raise ModelTrainingError(f"Prediction failed: {str(e)}")

    def predict_batch(self, feature_vectors):
        """
        Predict speakers for multiple feature vectors.

        Args:
            feature_vectors (list): List of feature vectors.

        Returns:
            list: List of (username, confidence) tuples.
        """
        if not self.is_trained:
            raise ModelTrainingError("Model not trained yet")

        predictions = []
        for feature in feature_vectors:
            username, confidence = self.predict(feature)
            predictions.append((username, confidence))

        return predictions

    def save_model(self, model_path=None, scaler_path=None):
        """
        Save trained model and scaler to files.

        Args:
            model_path (Path, optional): Path to save model pickle.
            scaler_path (Path, optional): Path to save scaler pickle.

        Returns:
            tuple: (model_path, scaler_path)

        Raises:
            ModelTrainingError: If saving fails.
        """
        try:
            if not self.is_trained:
                raise ModelTrainingError("Cannot save untrained model")

            model_path = Path(model_path or SPEAKER_MODEL_FILE)
            scaler_path = Path(scaler_path or SCALER_FILE)

            model_path.parent.mkdir(parents=True, exist_ok=True)
            scaler_path.parent.mkdir(parents=True, exist_ok=True)

            # Save model
            with open(model_path, "wb") as f:
                pickle.dump(self.model, f)
            print(f"✓ Model saved: {model_path}")

            # Save scaler
            with open(scaler_path, "wb") as f:
                pickle.dump(self.scaler, f)
            print(f"✓ Scaler saved: {scaler_path}")

            # Save label encoders as additional metadata
            metadata = {
                "label_encoder": self.label_encoder,
                "label_decoder": self.label_decoder,
                "model_type": self.model_type,
            }
            metadata_path = model_path.parent / "metadata.pkl"
            with open(metadata_path, "wb") as f:
                pickle.dump(metadata, f)
            print(f"✓ Metadata saved: {metadata_path}")

            return model_path, scaler_path

        except Exception as e:
            raise ModelTrainingError(f"Failed to save model: {str(e)}")


def train_model_from_database(model_type=MODEL_TYPE):
    """
    High-level function to train model using features from database.

    Args:
        model_type (str): Type of model ('svm' or 'random_forest').

    Returns:
        tuple: (model, scaler)

    Raises:
        ModelTrainingError: If training fails.
    """
    try:
        print(f"\n{'='*70}")
        print(f"Training Speaker Recognition Model from Database")
        print(f"{'='*70}\n")

        # Load features from database
        feature_manager = VoiceFeatureManager()
        feature_vectors, usernames = feature_manager.get_features_with_usernames()

        if len(feature_vectors) == 0:
            raise ModelTrainingError("No features found in database")

        print(f"Loaded {len(feature_vectors)} features from database\n")

        # Create and train model
        model = SpeakerRecognitionModel(model_type=model_type)
        model.train(feature_vectors, usernames)

        # Save model
        model.save_model()

        print(f"\n{'='*70}")
        print(f"Model training completed successfully!")
        print(f"{'='*70}\n")

        return model, model.scaler

    except Exception as e:
        raise ModelTrainingError(f"Failed to train model from database: {str(e)}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Speaker Recognition Model - Test Mode")
    print("=" * 70 + "\n")

    try:
        # Create synthetic training data
        print("Creating synthetic training data...\n")

        # 3 speakers, 5 samples each, 26 features
        np.random.seed(42)
        feature_vectors = []
        usernames = []

        for user_id, username in enumerate(["alice", "bob", "charlie"]):
            # Create speaker-specific features (add offset for each speaker)
            for _ in range(5):
                features = np.random.randn(26) + user_id * 0.5
                feature_vectors.append(features)
                usernames.append(username)

        print(f"Created {len(feature_vectors)} training samples\n")

        # Train SVM model
        print("Training SVM model...")
        svm_model = SpeakerRecognitionModel(model_type="svm")
        svm_model.train(feature_vectors, usernames)

        # Test predictions
        print("\nTesting predictions:")
        test_features = np.random.randn(26) + 0 * 0.5  # Similar to alice
        username, confidence = svm_model.predict(test_features)
        print(f"  Predicted: {username}, Confidence: {confidence:.4f}")

        # Save model
        print("\nSaving model...")
        svm_model.save_model()

        print("\n✓ Model training test completed!")

    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}", file=sys.stderr)
        sys.exit(1)
