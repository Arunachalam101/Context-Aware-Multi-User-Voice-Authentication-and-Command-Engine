"""
Configuration module for Voice Authentication and Command Engine.

Centralized management of paths, database settings, model configuration,
and application constants. All file paths in the project should reference
this module to ensure consistency.
"""

import os
from pathlib import Path

# ============================================================================
# PROJECT ROOT AND BASE PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
"""Absolute path to the project root directory."""

# ============================================================================
# DATA DIRECTORIES
# ============================================================================

DATA_DIR = PROJECT_ROOT / "data"
"""Path to the data directory."""

RAW_AUDIO_DIR = DATA_DIR / "raw_audio"
"""Path to store raw audio recordings."""

PROCESSED_FEATURES_DIR = DATA_DIR / "processed_features"
"""Path to store processed MFCC features."""

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DATABASE_DIR = PROJECT_ROOT / "database"
"""Path to the database directory."""

DATABASE_FILE = DATABASE_DIR / "voice_auth.db"
"""Path to the SQLite database file."""

# ============================================================================
# MODELS DIRECTORY
# ============================================================================

MODELS_DIR = PROJECT_ROOT / "models"
"""Path to the models directory."""

SPEAKER_MODEL_FILE = MODELS_DIR / "speaker_model.pkl"
"""Path to the trained speaker recognition model."""

SCALER_FILE = MODELS_DIR / "feature_scaler.pkl"
"""Path to the feature scaler (StandardScaler) for normalization."""

# ============================================================================
# LOGS DIRECTORY
# ============================================================================

LOGS_DIR = PROJECT_ROOT / "logs"
"""Path to the logs directory."""

APP_LOG_FILE = LOGS_DIR / "app.log"
"""Path to the main application log file."""

# ============================================================================
# VOSK SPEECH RECOGNITION
# ============================================================================

VOSK_MODEL_DIR = PROJECT_ROOT / "vosk_model" / "vosk-model-en-us-0.42-gigaspeech"
"""Path to VOSK offline speech recognition model."""

VOSK_MODEL_NAME = "vosk-model-en-us-0.42-gigaspeech"
"""Name of the VOSK model to use."""

# ============================================================================
# AUDIO RECORDING CONFIGURATION
# ============================================================================

SAMPLE_RATE = 16000
"""Audio sample rate in Hz (16 kHz for speech)."""

AUDIO_DURATION = 3
"""Duration of each audio recording in seconds."""

CHANNELS = 1
"""Number of audio channels (1 = mono)."""

DTYPE = "float32"
"""Audio data type."""

# ============================================================================
# MFCC FEATURE EXTRACTION
# ============================================================================

N_MFCC = 13
"""Number of MFCC coefficients to extract."""

N_FFT = 2048
"""FFT window size."""

HOP_LENGTH = 512
"""Number of samples between successive frames."""

# ============================================================================
# MACHINE LEARNING MODEL CONFIGURATION
# ============================================================================

MODEL_TYPE = "svm"
"""Type of ML model: 'svm' or 'random_forest'."""

SVM_KERNEL = "rbf"
"""Kernel type for SVM: 'rbf', 'linear', or 'poly'."""

SVM_C = 1.0
"""Regularization parameter for SVM."""

SVM_GAMMA = "scale"
"""Gamma parameter for SVM."""

RANDOM_FOREST_N_ESTIMATORS = 100
"""Number of trees in random forest."""

RANDOM_FOREST_MAX_DEPTH = 10
"""Maximum depth of trees in random forest."""

# ============================================================================
# TEXT-TO-SPEECH CONFIGURATION
# ============================================================================

TTS_RATE = 150
"""Speech rate for TTS (words per minute)."""

TTS_VOLUME = 1.0
"""Volume level for TTS (0.0 to 1.0)."""

TTS_VOICE = 0
"""Voice index for TTS (0 = first available voice)."""

# ============================================================================
# COMMAND EXECUTION CONFIGURATION
# ============================================================================

# Predefined commands and their corresponding actions
COMMANDS = {
    "open notepad": "notepad",
    "open calculator": "calc",
    "open cmd": "cmd",
    "tell time": "time",
    "system info": "systeminfo",
    "open file explorer": "explorer",
}
"""Mapping of voice commands to system actions."""

# ============================================================================
# DATABASE SCHEMA
# ============================================================================

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
"""SQL to create users table."""

CREATE_VOICE_FEATURES_TABLE = """
CREATE TABLE IF NOT EXISTS voice_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    feature_vector BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""
"""SQL to create voice features table."""

CREATE_COMMAND_LOGS_TABLE = """
CREATE TABLE IF NOT EXISTS command_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    command TEXT NOT NULL,
    status TEXT DEFAULT 'executed',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""
"""SQL to create command logs table."""

# ============================================================================
# APPLICATION CONSTANTS
# ============================================================================

APP_NAME = "Context-Aware Voice Authentication Engine"
"""Application name."""

APP_VERSION = "1.0.0"
"""Application version."""

AUTHENTICATION_THRESHOLD = 0.7
"""Confidence threshold for speaker authentication (0.0 to 1.0)."""

MIN_SAMPLES_FOR_TRAINING = 3
"""Minimum number of voice samples required per user to train."""

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def create_directories():
    """Create all required directories if they don't exist."""
    directories = [
        DATA_DIR,
        RAW_AUDIO_DIR,
        PROCESSED_FEATURES_DIR,
        DATABASE_DIR,
        MODELS_DIR,
        LOGS_DIR,
        VOSK_MODEL_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Directory ensured: {directory}")


def get_project_info():
    """Return project information."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "root": str(PROJECT_ROOT),
        "database": str(DATABASE_FILE),
        "models": str(MODELS_DIR),
    }


if __name__ == "__main__":
    # When run directly, display configuration info
    print(f"\n{'='*70}")
    print(f"Voice Authentication Engine - Configuration")
    print(f"{'='*70}\n")

    info = get_project_info()
    for key, value in info.items():
        print(f"{key.upper():<15}: {value}")

    print(f"\n{'='*70}")
    print("Creating required directories...")
    print(f"{'='*70}\n")

    create_directories()

    print(f"\n{'='*70}")
    print("Configuration initialized successfully!")
    print(f"{'='*70}\n")
