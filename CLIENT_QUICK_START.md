# 🎤 Voice Authentication System - Quick Start Guide

## One-Click Startup

**Simply double-click the file below to start the application:**

```
START_PROJECT.bat
```

That's it! The application will:
- ✓ Check system resources
- ✓ Verify all requirements are installed
- ✓ Load safely with memory protection
- ✓ Launch the GUI automatically

## First Time Setup

The first time you run the application:

1. **Register a User** - Click "Register New User"
   - Provide your name
   - Record 3+ voice samples (the system will guide you)
   - Wait for the model to train (takes 2-3 minutes)

2. **Authenticate** - Click "Authenticate"
   - Speak your registered voice
   - The system will verify you

3. **Give Commands** - After authentication, you can:
   - "open calculator"
   - "tell time"
   - "open notepad"
   - "system info"
   - And more!

## Requirements

- ✓ Windows 10/11
- ✓ Python 3.9+ (auto-installed packages if needed)
- ✓ Working microphone
- ✓ 2GB available memory
- ✓ 5GB free disk space (for VOSK model - downloads on first run)

## Troubleshooting

### Microphone Issues
- Ensure microphone is connected and enabled
- Check Windows Sound Settings (right-click speaker icon)
- Speak clearly and at normal volume
- Move closer to microphone if audio is too quiet

### Application Won't Start
- Close other applications (browsers, Discord, etc.)
- Check system has at least 500MB free memory
- Restart your computer

### Slow/Freezing
- Close unnecessary background applications
- This is normal on first startup while VOSK model loads (20-30 seconds)
- Subsequent startups are much faster

### Permission Denied
- Run Command Prompt as Administrator
- Navigate to the project folder
- Run: `START_PROJECT.bat`

## Getting Help

If you encounter issues:

1. **Check logs:**
   ```
   logs/voice_auth.log
   ```

2. **Run diagnostics:**
   ```
   python diagnose_system.py
   ```

3. **Test microphone:**
   ```
   python test_microphone.py
   ```

## Performance Tips

- **First run is slower** - VOSK model must load (20-30 seconds)
- **Speak clearly** - Neural network speech recognition improves with clear audio
- **Close other apps** - Frees up memory and CPU for optimal performance
- **Use USB microphone** - Better quality than laptop mic

## Architecture

This is a **fully offline** system:
- ✓ Speech recognition (VOSK) - No internet needed
- ✓ Speaker verification (ML models) - Runs locally
- ✓ Command execution - All local
- ✓ Data storage - Local SQLite database

**No data is sent to any cloud service or third party.**

---

**Version:** 1.0.0  
**Built with:** Python, Tkinter, VOSK, scikit-learn  
**License:** Proprietary
