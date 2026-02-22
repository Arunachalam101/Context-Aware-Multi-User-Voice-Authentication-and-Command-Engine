"""
Safe startup script with system resource checks.

Before launching the application, this script:
1. Checks available memory
2. Warns about high CPU/memory usage  
3. Suggests closing other applications if needed
4. Provides system health report
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.resource_monitor import ResourceMonitor


def check_system_health():
    """Check system health before launching application."""
    print("\n" + "=" * 70)
    print("SYSTEM HEALTH CHECK")
    print("=" * 70)
    
    status = ResourceMonitor.check_resources(verbose=True)
    
    print("\n" + "=" * 70)
    
    # Check if it's safe to proceed
    if status["memory_critical"]:
        print("\n❌ CRITICAL: System memory is critically low!")
        print("   This will likely cause the application to crash or your device to restart.")
        print("\n   Please close other applications and try again.")
        return False
    
    if status["cpu_critical"]:
        print("\n⚠️  CRITICAL: CPU usage is extremely high!")
        print("   Close other applications before running this.")
        return False
    
    if status["memory_warning"] or status["cpu_warning"]:
        print("\n⚠️  WARNING: System resources are constrained.")
        print("   The application might run slowly or be unable to load the speech model.")
        
        response = input("\nDo you want to continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            return False
    
    print("\n✓ System health check passed!")
    return True


def show_memory_tips():
    """Show tips for freeing memory."""
    print("\n" + "=" * 70)
    print("MEMORY OPTIMIZATION TIPS")
    print("=" * 70)
    print("\nTo free up memory, close:")
    print("  • Web browsers (Chrome, Firefox, Edge)")
    print("  • Video applications (YouTube, streaming services)")
    print("  • Large applications (Visual Studio, IDEs)")
    print("  • Unnecessary background processes")
    print("\nOr try restarting your computer before running the application.")


def main():
    """Main startup check."""
    print("\n🚀 Voice Authentication System - Safe Startup\n")
    
    # Check system health
    if not check_system_health():
        show_memory_tips()
        print("\nApplication startup cancelled.\n")
        return 1
    
    # All checks passed, launch application
    print("\n🎤 Launching application...\n")
    
    try:
        from app import main as app_main
        app_main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Application interrupted by user")
        return 0
    except Exception as e:
        print(f"\n❌ Application error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
