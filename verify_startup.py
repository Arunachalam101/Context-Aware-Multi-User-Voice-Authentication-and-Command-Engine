"""
Verify application startup and initialization without GUI.
Tests core initialization routines before GUI launch.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_startup_sequence():
    """Run startup verification without launching GUI."""
    
    print("\n" + "="*70)
    print(" VOICE AUTHENTICATION SYSTEM - STARTUP VERIFICATION")
    print("="*70 + "\n")
    
    try:
        # Step 1: Import config
        print("[1/5] Loading configuration...", end=" ")
        from utils.config import (
            PROJECT_ROOT as CONFIG_ROOT,
            DATABASE_FILE,
            create_directories,
            COMMANDS,
            SAMPLE_RATE,
            N_MFCC,
        )
        print("✓ OK")
        
        # Step 2: Create directories
        print("[2/5] Setting up directories...", end=" ")
        create_directories()
        print("✓ OK")
        
        # Step 3: Initialize database
        print("[3/5] Initializing database...", end=" ")
        from database.db_connection import init_database
        init_database()
        print("✓ OK")
        
        # Step 4: Verify training modules
        print("[4/5] Verifying ML modules...", end=" ")
        from ml.train_model import SpeakerRecognitionModel
        from ml.model_loader import ModelLoader
        from ml.predict_speaker import SpeakerAuthenticator
        print("✓ OK")
        
        # Step 5: Verify GUI modules
        print("[5/5] Verifying GUI modules...", end=" ")
        from gui.main_ui import MainWindow
        print("✓ OK")
        
        # Summary
        print("\n" + "="*70)
        print(" STARTUP VERIFICATION SUCCESSFUL")
        print("="*70)
        print(f"\n[INFO] Configuration:")
        print(f"  • Project Root: {CONFIG_ROOT}")
        print(f"  • Database: {DATABASE_FILE}")
        print(f"  • Sample Rate: {SAMPLE_RATE} Hz")
        print(f"  • MFCC Coefficients: {N_MFCC}")
        print(f"  • Predefined Commands: {len(COMMANDS)}")
        
        print(f"\n[OK] Application is ready to launch!")
        print(f"\n     Run: python app.py")
        print("\n" + "="*70 + "\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ FAILED")
        print(f"\n[ERROR] Startup verification failed:")
        print(f"  {str(e)}\n")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_startup_sequence()
    sys.exit(0 if success else 1)
