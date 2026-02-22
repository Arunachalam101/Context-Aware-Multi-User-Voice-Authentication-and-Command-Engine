#!/usr/bin/env python3
"""
Memory-Safe Voice Authentication System Launcher
===============================================

Prevents system crashes from large VOSK model loading by:
- Monitoring memory usage during startup
- Graceful degradation if memory is insufficient 
- Safe shutdown on memory warnings
"""

import os
import sys
import psutil
import time
import subprocess
from pathlib import Path

# Memory thresholds (in GB)
MINIMUM_FREE_RAM = 4.0  # Minimum 4GB free RAM required
WARNING_RAM_USAGE = 85  # Warning if system RAM > 85%
CRITICAL_RAM_USAGE = 95  # Force shutdown if system RAM > 95%

def check_system_memory():
    """Check if system has enough memory for VOSK model loading."""
    memory = psutil.virtual_memory()
    
    total_gb = memory.total / (1024**3)
    available_gb = memory.available / (1024**3)
    used_percent = memory.percent
    
    print(f"💾 System Memory Status:")
    print(f"   Total RAM: {total_gb:.1f} GB")
    print(f"   Available: {available_gb:.1f} GB") 
    print(f"   Used: {used_percent:.1f}%")
    
    if available_gb < MINIMUM_FREE_RAM:
        print(f"⚠️  WARNING: Only {available_gb:.1f} GB available (need {MINIMUM_FREE_RAM} GB)")
        print("   Close other applications before starting")
        return False
        
    if used_percent > WARNING_RAM_USAGE:
        print(f"⚠️  WARNING: High memory usage ({used_percent:.1f}%)")
        
    return True

def monitor_process_memory(process):
    """Monitor memory usage of running process."""
    try:
        memory_info = process.memory_info()
        memory_mb = memory_info.rss / (1024**2)
        
        system_memory = psutil.virtual_memory()
        if system_memory.percent > CRITICAL_RAM_USAGE:
            print(f"🚨 CRITICAL: System RAM at {system_memory.percent:.1f}% - Force shutdown!")
            process.terminate()
            return False
            
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False

def launch_voice_auth():
    """Launch Voice Authentication System with memory monitoring."""
    
    print("🔧 Memory-Safe Voice Authentication Launcher")
    print("=" * 50)
    
    # Check initial memory
    if not check_system_memory():
        response = input("\nContinue anyway? (y/N): ").lower()
        if response != 'y':
            print("❌ Launch cancelled for safety")
            return False
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print("\n🚀 Launching application...")
    print("📊 Memory monitoring active...")
    
    try:
        # Start the application
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], cwd=project_dir)
        
        # Monitor for first 60 seconds (critical VOSK loading period)
        start_time = time.time()
        while time.time() - start_time < 60:
            if process.poll() is not None:
                # Process finished
                if process.returncode == 0:
                    print("✅ Application started successfully!")
                else:
                    print(f"❌ Application failed (code {process.returncode})")
                return process.returncode == 0
                
            # Check memory every 2 seconds
            if not monitor_process_memory(process):
                print("❌ Memory monitoring failed - Application may have crashed")
                return False
                
            time.sleep(2)
            
        print("✅ Application passed critical startup phase - Running normally")
        
        # Wait for user to close or process to end
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down safely...")
            process.terminate()
            process.wait()
            
        return True
        
    except Exception as e:
        print(f"❌ Launch failed: {e}")
        return False

def main():
    """Main entry point."""
    success = launch_voice_auth()
    
    if success:
        print("\n🎉 Voice Authentication System completed successfully!")
    else:
        print("\n⚠️  Voice Authentication System encountered issues")
        print("💡 Try closing other applications and running again")
        
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()