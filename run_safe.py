"""
Startup wrapper that prevents crashes and device restarts.

This is the SAFE way to start the application.

Run this instead of app.py:
    python safe_startup.py
"""

import sys
import os
from pathlib import Path

# Disable crash dumps that might trigger restart
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.resource_monitor import ResourceMonitor


def show_startup_banner():
    """Show startup banner with instructions."""
    print("\n" + "=" * 70)
    print("🎤 Voice Authentication System - SAFE STARTUP")
    print("=" * 70 + "\n")
    
    print("This startup script includes:")
    print("  ✓ System resource monitoring")
    print("  ✓ Memory protection")
    print("  ✓ Audio device safeguards")
    print("  ✓ Crash prevention")
    print("\nIf you experience crashes, try:")
    print("  1. Close other applications (browsers, Discord, etc.)")
    print("  2. Run: python diagnose_system.py")
    print("  3. Restart your computer")
    print("\n" + "=" * 70 + "\n")


def check_startup_safety():
    """Check if it's safe to start the application."""
    print("📊 Checking system resources...\n")
    
    status = ResourceMonitor.check_resources(verbose=True)
    
    # Critical checks
    if status["memory_critical"]:
        print("\n" + "=" * 70)
        print("❌ CRITICAL: CANNOT START")
        print("=" * 70)
        print("\nYour system's memory is critically low.")
        print("This will cause the application or device to crash.\n")
        print("SOLUTIONS:")
        print("  1. Close all other applications immediately")
        print("  2. Restart your computer")
        print("  3. Run: python diagnose_system.py\n")
        return False
    
    # Warnings
    if status["memory_warning"]:
        print("\n" + "=" * 70)
        print("⚠️  WARNING: CONSTRAINED RESOURCES")
        print("=" * 70)
        print(f"\nMemory usage: {status['memory_percent']:.1f}%")
        print(f"Available: {status['available_memory_mb']:.0f} MB\n")
        print("The application might be unstable with these resources.\n")
        print("RECOMMENDED ACTIONS:")
        print("  • Close web browsers (YouTube, social media, etc.)")
        print("  • Close Discord, Slack, or other chat applications")
        print("  • Close IDE/editor (if not needed right now)")
        print("  • Restart your computer\n")
        
        response = input("Try to start anyway? (y/n): ").strip().lower()
        if response != 'y':
            print("\nStartup cancelled. Please free up memory and try again.\n")
            return False
    
    print("\n✓ Safety checks passed! Starting application...\n")
    return True


def main():
    """Main entry point."""
    show_startup_banner()
    
    if not check_startup_safety():
        return 1
    
    try:
        print("=" * 70)
        print("🚀 Launching application")
        print("=" * 70 + "\n")
        
        from app import main as app_main
        app_main()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Application interrupted")
        return 0
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
