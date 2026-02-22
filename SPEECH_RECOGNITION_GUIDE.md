# Speech Recognition Troubleshooting Guide 🎤

## Problem: "⚠️ No speech recognized"

When you execute a voice command, it shows "No speech recognized" instead of processing your command.

## Root Causes

### 1. Microphone Issues ❌
- Microphone not working
- Microphone input level too low
- Microphone not selected as default
- Microphone muted or disabled

### 2. Audio Quality Issues 🔊
- Speaking too quietly
- Too much background noise
- Audio distorted/clipped
- Microphone too far away

### 3. VOSK Issues 🎙️
- VOSK model not fully loaded
- VOSK not recognizing the speech format
- Audio format mismatch

## Diagnostic Steps

### Step 1: Test Microphone First
```bash
python test_microphone.py
```

This will:
- Check if microphone is detected
- Verify audio recording works
- Check audio levels
- Test VOSK speech recognition
- Provide specific feedback

### Step 2: Check Windows Microphone Settings
1. **Right-click** Volume icon in taskbar
2. **Select** "Open Volume mixer"
3. **Check:**
   - Microphone is not muted
   - Volume is at least 50%
   - Recording device is set as default

### Step 3: Test Microphone in Windows
1. **Settings** → **Sound**
2. **Scroll** to "Input"
3. **Check** microphone option
4. **Click** "Device properties"
5. **Go** to "Test your microphone"
6. **Speak** - should see volume indicator

## How to Fix

### If Microphone is Quiet
1. **Speak louder** (that's the easiest fix)
2. **Move microphone closer** (6-12 inches from mouth)
3. **Increase microphone input level** in Windows Settings
4. **Close background applications** (fans, music, videos)

### If Microphone Not Detected
1. **Check USB connection** (if external USB microphone)
2. **Check device drivers** → Manufacturer website
3. **Reinstall audio drivers**
4. **Restart computer**

### If VOSK Still Doesn't Recognize
1. **Speak more clearly**
2. **Use common keywords:**
   - "openapp"
   - "playmusic"
   - "closefile"
   - "createdir"
3. **Avoid whispers** - speak at normal volume
4. **English only** - Make sure speech is in English

## Audio Level Requirements

VOSK speech recognition works best with:
- **Minimum audio level:** 5% (loud whisper)
- **Optimal audio level:** 30-70% (normal speech)
- **Maximum audio level:** No clipping (< 1.0 normalized)

### Check Your Audio Level
```bash
python test_microphone.py
```

Look for these lines:
```
Max level: 0.45 ✓ Good
Max level: 0.02 ❌ Too quiet - speak louder!
Max level: 1.20 ❌ Clipping - reduce microphone input
```

## Commands to Test

Test with these simple commands:

| Command | What it does |
|---------|-------------|
| `openapp` | Opens an application |
| `closefile` | Closes a file |
| `playmusic` | Plays music |
| `checkstatus` | Checks system status |
| `createdir` | Creates a directory |
| `deletedir` | Deletes a directory |

## Testing Workflow

### 1. Run Diagnostic
```bash
python test_microphone.py
```

### 2. Fix Any Issues
Follow the feedback from the diagnostic

### 3. Run Application
```bash
python run_safe.py
```

### 4. Test Command
1. Click "🔐 Record Voice for Authentication"
2. Authenticate successfully
3. Click "🎤 Record Voice Command"
4. Say a command like "openapp"
5. Should see result in Command Result box

## If It Still Doesn't Work

1. **Restart computer** - Clears temporary issues
2. **Reinstall VOSK:** 
   ```bash
   pip uninstall vosk
   pip install vosk
   ```
3. **Check Python version:**
   ```bash
   python --version
   ```
   (Python 3.8+ recommended)

4. **Run diagnostic again:**
   ```bash
   python diagnose_system.py
   python test_microphone.py
   ```

## Support Information

### Collect Debug Info
When running the app, check console for messages like:
```
[DEBUG] Audio shape: (48000,), dtype: float32
[DEBUG] Audio min: -0.0045, max: 0.4321
[SUCCESS] Recognized text: 'openapp'
```

If you see debug output, copy it and refer back to these solutions.

## Tips for Best Results 💡

1. **Use default Windows microphone first**
   - Before trying USB microphones
   - Test with built-in laptop mic

2. **Clean environment**
   - Minimize background noise
   - Close doors
   - Stop fans if possible

3. **Proper microphone placement**
   - 6-12 inches from mouth
   - Slightly to the side
   - Avoid breathing directly into it

4. **Natural speech**
   - Don't rush
   - Speak clearly
   - Normal volume
   - Standard pronunciation

5. **Wait for VOSK to load**
   - First time: 20-30 seconds
   - Subsequent times: 5-10 seconds

## Quick Reference

| Issue | Solution |
|-------|----------|
| No microphone detected | Check hardware, install drivers |
| Microphone too quiet | Speak louder, move closer |
| No speech recognized | Test with `test_microphone.py` |
| Command not recognized | Use exact keywords (openapp, playmusic) |
| VOSK not loading | Close other apps, restart computer |

---

**Remember:** Most speech recognition issues are due to microphone audio levels. Test with `python test_microphone.py` first! 🎤
