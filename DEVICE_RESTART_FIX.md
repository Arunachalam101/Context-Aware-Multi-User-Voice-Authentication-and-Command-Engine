# Device Restart Prevention Guide 🛡️

If your device restarts while running this application, here's how to fix it:

## Root Cause

The VOSK speech recognition model is **large (~2.3GB)** and requires significant system memory to load. If your system is already consuming memory with other applications, loading VOSK can exhaust all available memory, causing:
- System freeze
- Application crash
- Device restart (Windows emergency shutdown)

## Solution: Free Up Memory First ✅

### Quick Fix (Do This First)
1. **Close ALL unnecessary applications:**
   - ❌ Web browsers (Chrome, Firefox, Edge, Safari)
   - ❌ Discord, Slack, Teams, Zoom
   - ❌ Spotify, YouTube, streaming apps
   - ❌ IDEs (VS Code, Visual Studio, PyCharm)
   - ❌ Video games
   
2. **Run the diagnostic:**
   ```bash
   python diagnose_system.py
   ```
   
3. **Check memory status:**
   ```bash
   python run_safe.py
   ```
   This will show available memory and warn if you don't have enough.

4. **Run the application:**
   ```bash
   python run_safe.py
   ```
   (Use `run_safe.py` instead of `app.py` for extra protection)

### Recommended Minimum
- **Available Memory:** 500 MB minimum, 1 GB optimal
- **CPU:** Not maxed out (below 80%)
- **Other Apps:** None using significant resources

## How to Check Memory

### Windows
1. Open Task Manager (Ctrl+Shift+Esc)
2. Click "Performance" tab
3. Look at "Memory" section
4. Check "Available" RAM

### Command Line
```bash
python diagnose_system.py
```

## Prevention Tips

### Before Running the Application
1. **Close everything except essential apps**
2. **Restart your computer** for best results
3. **Run diagnostic** to verify readiness
4. **Use safe startup** for monitoring

### While Running
- Monitor Task Manager
- If memory gets above 80%, close the recording/command windows
- Let VOSK finish loading (20-30 seconds) before using
- Don't record simultaneously on other devices

## Symptoms of Memory Issues

⚠️ **Watch for these signs:**
- Application freezes during VOSK load
- Progress bar stops responding
- Computer becomes very slow
- Fans running at maximum
- System restart (blue screen)

## Advanced Solutions

### Increase Virtual Memory (Windows)
1. Right-click "This PC" → Properties
2. Advanced system settings
3. "Environment Variables"
4. Increase pagefile size

### Disable Unnecessary Services
1. Open Services (services.msc)
2. Disable startup services you don't need
3. Restart computer

### Lower VOSK Memory Usage
If you have limited RAM (< 4GB):
1. Close ALL background apps
2. Use `diagnose_system.py` to verify readiness
3. Use `run_safe.py` for monitoring

## Still Having Issues?

1. **Run full diagnostic:**
   ```bash
   python diagnose_system.py
   ```

2. **Check Python version** (Python 3.8+ recommended):
   ```bash
   python --version
   ```

3. **Verify VOSK is installed:**
   ```bash
   python verify_vosk_setup.py
   ```

4. **Check system resources:**
   ```bash
   python run_safe.py
   ```

## System Recommendations

For smooth operation:
- **RAM:** 8GB or more
- **CPU:** Modern multi-core processor
- **Disk Space:** 5GB free
- **OS:** Windows 10/11, macOS, Linux

## Files for Help

- `run_safe.py` - Safe startup with memory checking
- `diagnose_system.py` - Full system diagnostics  
- `verify_vosk_setup.py` - VOSK model verification
- `safe_startup.py` - Initial startup checks

## Quick Reference

```bash
# Recommended: Always use this
python run_safe.py

# Or run diagnostics first
python diagnose_system.py
python run_safe.py

# Check VOSK setup
python verify_vosk_setup.py
```

---

**Remember:** Memory is the key limiting factor. Free up RAM before running! 🎤
