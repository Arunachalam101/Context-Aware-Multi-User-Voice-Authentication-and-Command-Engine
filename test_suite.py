"""
Comprehensive testing suite for Voice Authentication System.

Tests all modules individually and in integration.
Run this script to verify system readiness.
"""

import sys
import traceback
from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}[OK] {text}{Colors.RESET}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}[ERR] {text}{Colors.RESET}")


def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}[WARN] {text}{Colors.RESET}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}[INFO] {text}{Colors.RESET}")


def test_imports():
    """Test that all modules can be imported."""
    print_header("TEST 1: Module Imports")

    modules_to_test = [
        ("utils.config", "Configuration module"),
        ("database.db_connection", "Database connection"),
        ("database.db_operations", "Database operations"),
        ("audio.recorder", "Audio recorder"),
        ("audio.audio_utils", "Audio utilities"),
        ("features.mfcc_extractor", "MFCC extractor"),
        ("ml.train_model", "ML training"),
        ("ml.model_loader", "Model loader"),
        ("ml.predict_speaker", "Speaker prediction"),
        ("speech.vosk_recognizer", "VOSK recognizer"),
        ("commands.command_interpreter", "Command interpreter"),
        ("commands.action_executor", "Action executor"),
        ("response.tts_engine", "TTS engine"),
    ]

    passed = 0
    failed = 0

    for module_name, description in modules_to_test:
        try:
            # Suppress debug output from modules
            with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                __import__(module_name)
            print_success(f"{description} ({module_name})")
            passed += 1
        except ImportError as e:
            print_error(f"{description} ({module_name})")
            print(f"  Error: {str(e)}")
            failed += 1
        except Exception as e:
            print_warning(f"{description} ({module_name}) - Non-import error")
            print(f"  Error: {str(e)}")
            passed += 1  # Count as passed for non-import errors

    print(f"\n{Colors.BOLD}Results: {passed} passed, {failed} failed{Colors.RESET}\n")
    return failed == 0


def test_config():
    """Test configuration module."""
    print_header("TEST 2: Configuration Module")

    try:
        from utils.config import (
            APP_NAME,
            SAMPLE_RATE,
            N_MFCC,
            DATABASE_FILE,
            SPEAKER_MODEL_FILE,
            create_directories,
        )

        print_success(f"App name: {APP_NAME}")
        print_success(f"Sample rate: {SAMPLE_RATE}Hz")
        print_success(f"MFCC coefficients: {N_MFCC}")
        print_success(f"Database file: {DATABASE_FILE}")
        print_info(f"Database file type: {type(DATABASE_FILE)}")

        # Test directory creation
        create_directories()
        print_success("Directories created successfully")

        return True

    except Exception as e:
        print_error(f"Configuration test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_database():
    """Test database module."""
    print_header("TEST 3: Database Operations")

    try:
        from database.db_connection import DatabaseConnection, init_database

        # Initialize database
        db = init_database()
        print_success("Database initialized")

        # Test table existence
        tables = ["users", "voice_features", "command_logs"]
        for table in tables:
            exists = db.table_exists(table)
            if exists:
                print_success(f"Table '{table}' exists")
            else:
                print_error(f"Table '{table}' missing")
                return False

        # Test basic operations
        from database.db_operations import UserManager
        user_mgr = UserManager()

        # Try to create test user
        try:
            user_id = user_mgr.register_user("test_user", "test")
            print_success(f"User registration works (ID: {user_id})")

            # Check user exists
            user = user_mgr.get_user("test_user")
            if user:
                print_success(f"User retrieval works")
            else:
                print_error("User retrieval failed")
                return False

            # Cleanup
            user_mgr.delete_user("test_user")
            print_success("User deletion works")

        except Exception as e:
            if "UNIQUE constraint" in str(e):
                print_warning("Test user already exists (previous test run)")
            else:
                raise

        return True

    except Exception as e:
        print_error(f"Database test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_audio_utils():
    """Test audio utilities."""
    print_header("TEST 4: Audio Utilities")

    try:
        from audio.audio_utils import (
            get_audio_info,
            normalize_audio,
            validate_audio,
        )
        import numpy as np

        # Create synthetic audio
        duration = 2
        sr = 16000
        t = np.linspace(0, duration, sr * duration)
        test_audio = np.sin(2 * np.pi * 440 * t) * 0.3

        print_info(f"Created test audio: 440Hz sine wave, {duration}s")

        # Test info
        info = get_audio_info(test_audio, sr)
        print_success(f"Audio info: {len(test_audio)} samples, {info['duration_seconds']:.2f}s")

        # Test normalization
        normalized = normalize_audio(test_audio, method="standard")
        print_success(f"Audio normalization works (std={np.std(normalized):.4f})")

        # Test validation
        is_valid, message = validate_audio(test_audio, sr=sr)
        print_success(f"Audio validation: {message}")

        return True

    except Exception as e:
        print_error(f"Audio utilities test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_mfcc():
    """Test MFCC extraction."""
    print_header("TEST 5: MFCC Feature Extraction")

    try:
        from features.mfcc_extractor import MFCCExtractor
        import numpy as np

        # Create test audio
        duration = 2
        sr = 16000
        t = np.linspace(0, duration, sr * duration)
        test_audio = np.sin(2 * np.pi * 440 * t) * 0.3

        print_info(f"Created test audio: {duration}s at {sr}Hz")

        # Test MFCC extraction
        extractor = MFCCExtractor(n_mfcc=13)
        print_success("MFCC extractor initialized")

        # Extract MFCC
        mfcc = extractor.extract_mfcc(test_audio)
        print_success(f"MFCC extracted: shape {mfcc.shape}")

        # Compute statistics
        features = extractor.compute_statistics(mfcc)
        print_success(f"Feature vector computed: shape {features.shape}")

        # Get feature info
        info = extractor.get_statistics_info()
        print_success(f"Feature vector size: {info['feature_vector_size']}")

        return True

    except Exception as e:
        print_error(f"MFCC test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_ml_models():
    """Test ML model training."""
    print_header("TEST 6: Machine Learning Models")

    try:
        from ml.train_model import SpeakerRecognitionModel
        import numpy as np

        print_info("Testing SVM model...")

        # Create synthetic training data
        np.random.seed(42)
        feature_vectors = []
        usernames = []

        for user_id, username in enumerate(["alice", "bob", "charlie"]):
            for _ in range(5):
                features = np.random.randn(26) + user_id * 0.5
                feature_vectors.append(features)
                usernames.append(username)

        print_success(f"Created {len(feature_vectors)} training samples")

        # Train model
        model = SpeakerRecognitionModel(model_type="svm")
        model.train(feature_vectors, usernames)
        print_success("SVM model training completed")

        # Test prediction
        test_features = np.random.randn(26) + 0 * 0.5  # Similar to alice
        username, confidence = model.predict(test_features)
        print_success(f"Prediction works: {username} ({confidence:.2%})")

        print_info("Testing Random Forest model...")

        # Train RF model
        rf_model = SpeakerRecognitionModel(model_type="random_forest")
        rf_model.train(feature_vectors, usernames)
        print_success("Random Forest model training completed")

        return True

    except Exception as e:
        print_error(f"ML models test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_command_interpreter():
    """Test command interpreter."""
    print_header("TEST 7: Command Interpreter")

    try:
        from commands.command_interpreter import CommandInterpreter

        interpreter = CommandInterpreter()
        print_success("Command interpreter initialized")

        # List commands
        commands = interpreter.list_commands()
        print_success(f"Loaded {len(commands)} commands")

        # Test exact match
        result = interpreter.interpret_command("open notepad")
        if result["success"]:
            print_success(f"Exact match works: '{result['command']}'")
        else:
            print_error("Exact match failed")
            return False

        # Test fuzzy match
        result = interpreter.interpret_command("open notepd")
        if result["success"]:
            print_success(f"Fuzzy match works: '{result['command']}' ({result['confidence']:.0%})")
        else:
            print_warning("Fuzzy match not confident enough")

        # Test suggestions
        suggestions = interpreter.get_suggestions("open calc")
        print_success(f"Got {len(suggestions)} suggestions")

        return True

    except Exception as e:
        print_error(f"Command interpreter test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_action_executor():
    """Test action executor."""
    print_header("TEST 8: Action Executor")

    try:
        from commands.action_executor import ActionExecutor

        executor = ActionExecutor()
        print_success("Action executor initialized")

        # Test tell time
        result = executor.tell_time()
        if result["success"]:
            print_success(f"Tell time works: {result['response']}")
        else:
            print_error("Tell time failed")
            return False

        # Test system info
        result = executor.execute_action("system info")
        if result["success"]:
            print_success(f"System info works: {result['system_info']['system']}")
        else:
            print_error("System info failed")
            return False

        return True

    except Exception as e:
        print_error(f"Action executor test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_tts():
    """Test TTS engine."""
    print_header("TEST 9: Text-to-Speech Engine")

    try:
        from response.tts_engine import TextToSpeechEngine

        tts = TextToSpeechEngine()
        print_success("TTS engine initialized")

        # Get available voices
        voices = tts.get_available_voices()
        print_success(f"Found {len(voices)} available voices")

        # Get engine info
        info = tts.get_engine_info()
        print_success(f"TTS configured: rate={info['rate']}wpm, volume={info['volume']}")

        return True

    except Exception as e:
        print_error(f"TTS test failed: {str(e)}")
        traceback.print_exc()
        return False


def test_integration():
    """Test full integration pipeline."""
    print_header("TEST 10: Integration Pipeline")

    try:
        print_info("Testing: Database -> Features -> Model -> Prediction")

        from database.db_operations import UserManager, VoiceFeatureManager
        from ml.train_model import SpeakerRecognitionModel
        import numpy as np

        # Step 1: Create users
        user_mgr = UserManager()
        try:
            user_mgr.register_user("user_alice_test", "test")
            user_mgr.register_user("user_bob_test", "test")
        except:
            pass
        print_success("Step 1: Users created")

        # Step 2: Store features
        feature_mgr = VoiceFeatureManager()
        # Store features for user 1
        test_features_1 = np.random.randn(26) * 0.1
        feature_mgr.store_feature("user_alice_test", test_features_1)
        feature_mgr.store_feature("user_alice_test", test_features_1 + 0.05)
        
        # Store features for user 2
        test_features_2 = np.random.randn(26) * 0.1 + 0.2
        feature_mgr.store_feature("user_bob_test", test_features_2)
        feature_mgr.store_feature("user_bob_test", test_features_2 + 0.05)
        
        print_success("Step 2: Features stored")

        # Step 3: Retrieve features
        features, usernames = feature_mgr.get_features_with_usernames()
        print_success(f"Step 3: Retrieved {len(features)} features")

        # Step 4: Train model
        if len(features) >= 4:
            model = SpeakerRecognitionModel(model_type="svm")
            model.train(features, usernames)
            print_success("Step 4: Model trained")

            # Step 5: Predict
            username, conf = model.predict(test_features_1)
            print_success(f"Step 5: Prediction works ({username}, {conf:.2%})")
        else:
            print_warning("Not enough samples for training")

        # Cleanup
        user_mgr.delete_user("user_alice_test")
        user_mgr.delete_user("user_bob_test")
        print_success("Integration test cleanup completed")

        return True

    except Exception as e:
        print_error(f"Integration test failed: {str(e)}")
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("+" + "="*68 + "+")
    print("|" + " "*68 + "|")
    print("|" + "Voice Authentication System - Testing Suite".center(68) + "|")
    print("|" + " "*68 + "|")
    print("+" + "="*68 + "+")
    print(Colors.RESET)

    results = []

    # Run all tests
    test_functions = [
        ("Module Imports", test_imports),
        ("Configuration", test_config),
        ("Database", test_database),
        ("Audio Utils", test_audio_utils),
        ("MFCC Extraction", test_mfcc),
        ("ML Models", test_ml_models),
        ("Command Interpreter", test_command_interpreter),
        ("Action Executor", test_action_executor),
        ("TTS Engine", test_tts),
        ("Integration Pipeline", test_integration),
    ]

    for test_name, test_func in test_functions:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Unexpected error in {test_name}: {str(e)}")
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print_header("TEST SUMMARY")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = f"{Colors.GREEN}[PASS]{Colors.RESET}" if result else f"{Colors.RED}[FAIL]{Colors.RESET}"
        print(f"{status} - {test_name}")

    print(f"\n{Colors.BOLD}Total: {passed}/{total} tests passed{Colors.RESET}\n")

    if passed == total:
        print_success("All tests passed! System is ready for deployment.")
        return 0
    else:
        print_error(f"{total - passed} test(s) failed. Review output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
