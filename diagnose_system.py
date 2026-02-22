"""
Diagnostic tool to identify potential crash causes.

Analyzes:
- Memory leaks
- Resource consumption
- Audio device issues
- System stability
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.resource_monitor import ResourceMonitor
import psutil
import sounddevice as sd


def check_memory_leaks():
    """Check for potential memory leaks in code."""
    print("\n" + "=" * 70)
    print("MEMORY LEAK ANALYSIS")
    print("=" * 70)
    
    # Get process info
    process = psutil.Process()
    mem_info = process.memory_info()
    
    print(f"\nCurrent process memory usage:")
    print(f"  RSS (Physical): {mem_info.rss / (1024*1024):.1f} MB")
    print(f"  VMS (Virtual):  {mem_info.vms / (1024*1024):.1f} MB")
    
    # Check for potential issues
    if mem_info.rss > 500:
        print("\n⚠️  WARNING: High memory usage detected!")
        print("   This might indicate a memory leak in the application.")
    else:
        print("\n✓ Memory usage appears normal")
    
    return mem_info.rss < 800  # Flag if using more than 800MB


def check_audio_device():
    """Check audio device status."""
    print("\n" + "=" * 70)
    print("AUDIO DEVICE CHECK")
    print("=" * 70)
    
    try:
        devices = sd.query_devices()
        if len(devices) == 0:
            print("\n❌ No audio devices detected!")
            return False
        
        print(f"\n✓ Audio devices available: {len(devices)}")
        print(f"  Default device: {sd.default.device}")
        print(f"  Input devices: {len([d for d in devices if d['max_input_channels'] > 0])}")
        return True
    except Exception as e:
        print(f"\n❌ Audio device error: {e}")
        return False


def check_vosk_file_access():
    """Check if VOSK model files are accessible."""
    print("\n" + "=" * 70)
    print("VOSK MODEL FILE ACCESS")
    print("=" * 70)
    
    from utils.config import VOSK_MODEL_DIR
    
    if not VOSK_MODEL_DIR.exists():
        print(f"\n❌ VOSK model directory not found:")
        print(f"   {VOSK_MODEL_DIR}")
        return False
    
    # Check if required files exist
    required = ['am', 'conf', 'graph', 'ivector']
    missing = [d for d in required if not (VOSK_MODEL_DIR / d).exists()]
    
    if missing:
        print(f"\n❌ Missing VOSK model directories: {', '.join(missing)}")
        return False
    
    print(f"\n✓ VOSK model files are accessible")
    print(f"  Location: {VOSK_MODEL_DIR}")
    return True


def check_system_stability():
    """Check for system stability issues."""
    print("\n" + "=" * 70)
    print("SYSTEM STABILITY CHECK")
    print("=" * 70)
    
    # Check for high CPU throttling
    try:
        # Get CPU frequency
        freq = psutil.cpu_freq()
        print(f"\nCPU Frequency:")
        print(f"  Current: {freq.current:.0f} MHz")
        print(f"  Max:     {freq.max:.0f} MHz")
        print(f"  Min:     {freq.min:.0f} MHz")
        
        if freq.current < freq.max * 0.5:
            print("\n⚠️  WARNING: CPU is running below 50% of max frequency!")
            print("   This might indicate thermal throttling or power management.")
            return False
    except Exception:
        pass
    
    # Check system temperature (Linux only)
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            print(f"\nSystem Temperatures:")
            for sensor, readings in temps.items():
                for reading in readings:
                    print(f"  {sensor}: {reading.current:.1f}°C")
    except Exception:
        pass
    
    print("\n✓ System stability check complete")
    return True


def generate_report():
    """Generate a comprehensive diagnostic report."""
    print("\n" + "=" * 70)
    print("DIAGNOSTIC REPORT")
    print("=" * 70 + "\n")
    
    # Run all checks
    mem_ok = not check_memory_leaks()
    audio_ok = check_audio_device()
    vosk_ok = check_vosk_file_access()
    system_ok = check_system_stability()
    
    # Resource check
    status = ResourceMonitor.check_resources(verbose=False)
    resource_ok = not (status["memory_critical"] or status["cpu_critical"])
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    checks = {
        "Memory OK": mem_ok,
        "Audio Device OK": audio_ok,
        "VOSK Model OK": vosk_ok,
        "System Stable": system_ok,
        "Resources OK": resource_ok,
    }
    
    print()
    for check, result in checks.items():
        status_icon = "✓" if result else "❌"
        print(f"  {status_icon} {check}")
    
    all_ok = all(checks.values())
    
    print("\n" + "=" * 70)
    if all_ok:
        print("✓ All checks passed! Application should run normally.")
    else:
        print("❌ Some checks failed. See details above.")
        print("\nIf the application crashes or device restarts, try:")
        print("  1. Close other applications to free memory")
        print("  2. Restart your computer")
        print("  3. Run this diagnostic again to verify all checks pass")
    print("=" * 70 + "\n")
    
    return all_ok


if __name__ == "__main__":
    success = generate_report()
    sys.exit(0 if success else 1)
