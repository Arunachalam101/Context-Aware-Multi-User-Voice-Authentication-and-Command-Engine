"""
Debug script to test AuthenticationWindow initialization.
Runs in console to show all errors and debug messages.
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

import tkinter as tk
from gui.auth_ui import AuthenticationWindow

def main():
    """Test AuthenticationWindow initialization."""
    print("=" * 60)
    print("AUTH WINDOW INITIALIZATION TEST")
    print("=" * 60)
    
    print("\n[1] Creating root window...")
    root = tk.Tk()
    
    print("[2] Creating AuthenticationWindow...")
    try:
        auth_window = AuthenticationWindow(root)
        print("[3] AuthenticationWindow created successfully")
        
        print(f"\n[4] Checking recognizer status:")
        print(f"    Recognizer object: {auth_window.recognizer}")
        if auth_window.recognizer is None:
            print("    ⚠️  Recognizer is None")
        else:
            print(f"    ✓ Recognizer initialized: {type(auth_window.recognizer)}")
        
        print("[5] Starting GUI loop (close window to exit)...")
        root.mainloop()
        
    except Exception as e:
        print(f"[ERROR] Failed to create AuthenticationWindow: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
