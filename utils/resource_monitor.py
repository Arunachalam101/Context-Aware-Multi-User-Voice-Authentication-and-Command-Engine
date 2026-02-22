"""
System resource monitor to prevent crashes and device restart.

Monitors:
- Memory usage
- CPU usage
- Audio device status
- Thread count

Provides warnings and safeguards before resources exhaust.
"""

import psutil
import warnings


class ResourceMonitor:
    """Monitor system resources and provide warnings."""

    # Resource thresholds
    MEMORY_WARNING_THRESHOLD = 80  # Percent
    MEMORY_CRITICAL_THRESHOLD = 90  # Percent
    CPU_WARNING_THRESHOLD = 85  # Percent
    CPU_CRITICAL_THRESHOLD = 95  # Percent

    @staticmethod
    def get_memory_usage():
        """Get current memory usage percentage."""
        try:
            return psutil.virtual_memory().percent
        except Exception:
            return 0

    @staticmethod
    def get_cpu_usage():
        """Get current CPU usage percentage."""
        try:
            return psutil.cpu_percent(interval=0.1)
        except Exception:
            return 0

    @staticmethod
    def get_available_memory_mb():
        """Get available memory in MB."""
        try:
            return psutil.virtual_memory().available / (1024 * 1024)
        except Exception:
            return 0

    @staticmethod
    def get_thread_count():
        """Get current thread count."""
        try:
            return len(psutil.Process().threads())
        except Exception:
            return 0

    @classmethod
    def check_resources(cls, verbose=False):
        """
        Check system resources and return status.

        Args:
            verbose (bool): Print detailed information.

        Returns:
            dict: Resource status information.
        """
        memory_pct = cls.get_memory_usage()
        cpu_pct = cls.get_cpu_usage()
        mem_mb = cls.get_available_memory_mb()
        threads = cls.get_thread_count()

        status = {
            "memory_percent": memory_pct,
            "cpu_percent": cpu_pct,
            "available_memory_mb": mem_mb,
            "thread_count": threads,
            "memory_warning": memory_pct > cls.MEMORY_WARNING_THRESHOLD,
            "memory_critical": memory_pct > cls.MEMORY_CRITICAL_THRESHOLD,
            "cpu_warning": cpu_pct > cls.CPU_WARNING_THRESHOLD,
            "cpu_critical": cpu_pct > cls.CPU_CRITICAL_THRESHOLD,
        }

        if verbose:
            print("\n📊 SYSTEM RESOURCE STATUS:")
            print(f"  Memory: {memory_pct:.1f}% used ({mem_mb:.0f} MB available)")
            print(f"  CPU: {cpu_pct:.1f}% used")
            print(f"  Threads: {threads}")

            if status["memory_critical"]:
                print("  ⚠️  CRITICAL: Memory usage is dangerously high!")
            elif status["memory_warning"]:
                print("  ⚠️  WARNING: Memory usage is high")

            if status["cpu_critical"]:
                print("  ⚠️  CRITICAL: CPU usage is extremely high!")
            elif status["cpu_warning"]:
                print("  ⚠️  WARNING: CPU usage is high")

        return status

    @classmethod
    def check_vosk_safety(cls):
        """
        Check if it's safe to load VOSK.

        VOSK requires ~500MB-1GB memory.

        Returns:
            tuple: (is_safe, message)
        """
        status = cls.check_resources()
        mem_mb = status["available_memory_mb"]

        # VOSK needs at least 500MB to load safely
        if mem_mb < 500:
            return False, (
                f"Not enough memory to load VOSK safely.\n"
                f"Available: {mem_mb:.0f} MB\n"
                f"Required: 500+ MB\n\n"
                f"Please close other applications and try again."
            )

        # Warn if memory is getting tight
        if status["memory_warning"]:
            return True, (
                f"Memory usage is high ({status['memory_percent']:.1f}%).\n"
                f"VOSK might consume significant resources.\n"
                f"Loading will continue, but monitor memory usage."
            )

        return True, None


def install_resource_monitor():
    """Ensure psutil is installed."""
    try:
        import psutil
        return True
    except ImportError:
        print("[WARNING] psutil not installed. Memory monitoring disabled.")
        print("Install with: pip install psutil")
        return False


# Try to install on import
try:
    import psutil
except ImportError:
    print("[WARNING] psutil not installed. Installing...")
    import subprocess
    try:
        subprocess.check_call(["pip", "install", "psutil"])
        import psutil
    except Exception as e:
        print(f"[ERROR] Failed to install psutil: {e}")
        print("Install manually with: pip install psutil")
