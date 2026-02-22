"""
Example Usage Scripts - Shows how to use the system programmatically
"""

# ============================================================================
# EXAMPLE 1: Register a User Programmatically
# ============================================================================

def example_register_user():
    """Example: Register a new user without GUI"""
    from database.db_operations import UserManager, VoiceFeatureManager
    import numpy as np
    
    # Initialize managers
    user_mgr = UserManager()
    feature_mgr = VoiceFeatureManager()
    
    # Create a new user
    username = "demo_user"
    password = "demo_password"
    
    try:
        user_id = user_mgr.register_user(username, password)
        print(f"✓ User registered: {username} (ID: {user_id})")
        
        # Simulate storing voice features (normally from AudioRecorder)
        for i in range(4):
            # In real use, this would come from MFCC extraction
            fake_feature = np.random.randn(26) * 0.1 + 0.5
            feature_mgr.store_feature(username, fake_feature)
            print(f"  ✓ Feature {i+1} stored")
        
        return user_id
        
    except ValueError as e:
        print(f"✗ Error: {str(e)}")
        return None


# ============================================================================
# EXAMPLE 2: Train Model Programmatically
# ============================================================================

def example_train_model():
    """Example: Train ML model without GUI"""
    from database.db_operations import VoiceFeatureManager
    from ml.train_model import SpeakerRecognitionModel
    
    # Get features from database
    feature_mgr = VoiceFeatureManager()
    features, usernames = feature_mgr.get_features_with_usernames()
    
    if len(features) < 6:  # Need ≥2 speakers with ≥3 samples each
        print(f"✗ Not enough features: {len(features)} (need ≥6)")
        return None
    
    print(f"Training model with {len(features)} features from {len(set(usernames))} speakers...")
    
    # Create and train model
    model = SpeakerRecognitionModel(model_type="svm")
    model.train(features, usernames)
    model.save_model()
    
    print("✓ Model trained and saved to: models/speaker_model.pkl")
    return model


# ============================================================================
# EXAMPLE 3: Authenticate User Programmatically
# ============================================================================

def example_authenticate():
    """Example: Authenticate a speaker without GUI"""
    from ml.predict_speaker import SpeakerAuthenticator
    import numpy as np
    
    # Load the trained model
    auth = SpeakerAuthenticator()
    
    # Simulate a voice feature (normally from MFCC extraction)
    sample_feature = np.array([0.1, 0.2, -0.1, 0.3, 0.0, 0.2, -0.05, 0.15, 
                               0.1, -0.1, 0.2, 0.3, -0.2, 0.1, 0.0, 0.2,
                               0.1, 0.15, -0.1, 0.2, 0.3, -0.1, 0.15, 0.0,
                               0.2, -0.05])
    
    # Authenticate
    result = auth.authenticate(sample_feature, threshold=0.7)
    
    if result['authenticated']:
        print(f"✓ Authenticated as: {result['username']}")
        print(f"  Confidence: {result['confidence']:.2%}")
    else:
        print(f"✗ Authentication failed")
        print(f"  Closest match: {result['predicted_user']}")
        print(f"  Confidence: {result['confidence']:.2%}")
    
    return result


# ============================================================================
# EXAMPLE 4: Interpret Command Programmatically
# ============================================================================

def example_interpret_command():
    """Example: Interpret voice commands without GUI"""
    from commands.command_interpreter import CommandInterpreter
    
    # Create interpreter
    interpreter = CommandInterpreter()
    
    # Test commands
    test_inputs = [
        "what is the time",           # Exact match
        "tell me the time",           # Exact match
        "whats the current time",     # Fuzzy match
        "open notepad",               # Exact match
        "open note pad",              # Fuzzy match
        "open chrome",                # Exact match
        "open chrome browser",        # Fuzzy match
        "unknown command",            # No match
    ]
    
    print("Command Interpretation Examples:")
    print("-" * 70)
    
    for command_text in test_inputs:
        result = interpreter.interpret_command(command_text)
        
        if result['success']:
            print(f"'{command_text}'")
            print(f"  ✓ Matched: {result['command']} ({result['confidence']:.0%})")
            print(f"  → Action: {result['action']}")
        else:
            print(f"'{command_text}'")
            print(f"  ✗ No match")
            if result['suggestions']:
                print(f"  → Suggestions: {', '.join(result['suggestions'][:3])}")
        print()


# ============================================================================
# EXAMPLE 5: Execute Commands Programmatically
# ============================================================================

def example_execute_commands():
    """Example: Execute system commands without GUI"""
    from commands.action_executor import ActionExecutor
    
    executor = ActionExecutor()
    
    # Test available actions
    print("Available Commands:")
    print("-" * 70)
    
    # Get current time
    time_result = executor.execute_action("tell_time", {})
    print(f"✓ Tell Time: {time_result}")
    
    # Get system info
    info = executor.execute_action("system_info", {})
    print(f"✓ System Info: {info}")
    
    # Note: open_app requires actual app to be installed
    # Example: executor.execute_action("open_app", {"app": "notepad.exe"})


# ============================================================================
# EXAMPLE 6: Full Pipeline (Database → Train → Predict)
# ============================================================================

def example_full_pipeline():
    """Example: Complete voice authentication workflow"""
    from database.db_operations import UserManager, VoiceFeatureManager
    from ml.train_model import SpeakerRecognitionModel
    from ml.predict_speaker import SpeakerAuthenticator
    import numpy as np
    
    print("\n" + "="*70)
    print("FULL PIPELINE EXAMPLE")
    print("="*70 + "\n")
    
    # Step 1: Register users
    print("[STEP 1] Register users...")
    user_mgr = UserManager()
    feature_mgr = VoiceFeatureManager()
    
    try:
        # Create users if not exist
        user_mgr.register_user("alice", "password1")
        user_mgr.register_user("bob", "password2")
    except:
        pass  # Users may already exist
    
    print("  ✓ Users registered/verified")
    
    # Step 2: Store features
    print("\n[STEP 2] Store voice features...")
    
    # Create distinct feature patterns for each user
    np.random.seed(42)
    for username in ["alice", "bob"]:
        for i in range(4):
            if username == "alice":
                # Alice's voice pattern
                feature = np.random.randn(26) * 0.1 + 0.3
            else:
                # Bob's voice pattern
                feature = np.random.randn(26) * 0.1 - 0.3
            
            feature_mgr.store_feature(username, feature)
    
    print("  ✓ 8 features stored (4 per user)")
    
    # Step 3: Train model
    print("\n[STEP 3] Train speaker model...")
    features, usernames = feature_mgr.get_features_with_usernames()
    
    model = SpeakerRecognitionModel(model_type="svm")
    model.train(features, usernames)
    model.save_model()
    print("  ✓ Model trained and saved")
    
    # Step 4: Authenticate
    print("\n[STEP 4] Authenticate speakers...")
    auth = SpeakerAuthenticator()
    
    # Test with Alice's pattern
    alice_feature = np.random.randn(26) * 0.1 + 0.3
    result = auth.authenticate(alice_feature)
    print(f"  ✓ Recognized: {result['predicted_user']} ({result['confidence']:.2%})")
    
    # Test with Bob's pattern
    bob_feature = np.random.randn(26) * 0.1 - 0.3
    result = auth.authenticate(bob_feature)
    print(f"  ✓ Recognized: {result['predicted_user']} ({result['confidence']:.2%})")
    
    print("\n[OK] Pipeline complete!")
    print("="*70 + "\n")


# ============================================================================
# EXAMPLE 7: Database Operations
# ============================================================================

def example_database_operations():
    """Example: Common database operations"""
    from database.db_operations import UserManager, VoiceFeatureManager
    
    user_mgr = UserManager()
    feature_mgr = VoiceFeatureManager()
    
    print("Database Operations Examples:")
    print("-" * 70)
    
    # List all users
    users = user_mgr.list_all_users()
    print(f"\n[Users Registered: {len(users)}]")
    for user in users[:5]:  # Show first 5
        print(f"  • {user['username']} (ID: {user['id']})")
    
    # Count features
    features, _ = feature_mgr.get_features_with_usernames()
    print(f"\n[Total Voice Features: {len(features)}]")
    
    # Get specific user's features
    if users:
        username = users[0]['username']
        user_features = feature_mgr.get_features_for_user(username)
        print(f"\n[Features for '{username}': {len(user_features)}]")


# ============================================================================
# MAIN - Run Examples
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Prevent imports from showing debug print statements
    from io import StringIO
    from contextlib import redirect_stdout
    
    print("\n" + "="*70)
    print("VOICE AUTHENTICATION - EXAMPLE USAGE SCRIPTS")
    print("="*70)
    
    # Suppress module import output
    with redirect_stdout(StringIO()):
        from database.db_operations import UserManager
    
    print("\nAvailable examples:")
    print("  1. Register user")
    print("  2. Train model")
    print("  3. Authenticate user")
    print("  4. Interpret commands")
    print("  5. Execute actions")
    print("  6. Full pipeline demo")
    print("  7. Database operations")
    print("  8. Run all examples")
    print("\nUsage: python examples.py 1-8")
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        
        try:
            with redirect_stdout(StringIO()):
                from database.db_operations import VoiceFeatureManager
                from ml.train_model import SpeakerRecognitionModel
            
            if choice == "1":
                example_register_user()
            elif choice == "2":
                example_train_model()
            elif choice == "3":
                example_authenticate()
            elif choice == "4":
                example_interpret_command()
            elif choice == "5":
                example_execute_commands()
            elif choice == "6":
                example_full_pipeline()
            elif choice == "7":
                example_database_operations()
            elif choice == "8":
                example_register_user()
                print("\n")
                example_interpret_command()
                print("\n")
                example_execute_commands()
                print("\n")
                example_database_operations()
            else:
                print(f"Invalid choice: {choice}")
        except ImportError as e:
            print(f"Error: Missing module - {str(e)}")
            print("Run: pip install -r requirements.txt")
    else:
        print("\nRun an example: python examples.py 1")
