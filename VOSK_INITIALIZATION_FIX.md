# VOSK Model Initialization Error - Fix Guide

## Problem
When running the app, you get this error:
```
Failed to initialize VOSK model
VOSK model not found at vosk_model/
```

Or authentication/commands don't work even though the app started.

---

## Root Causes

| Cause | Why | Fix |
|-------|-----|-----|
| **Download incomplete** | Network interrupted | Run `fix_vosk_model.py` |
| **vosk_model corrupted** | Extraction failed | Run `fix_vosk_model.py` to re-download |
| **vosk package not installed** | pip install failed | Run `START.bat` again |
| **Missing model files** | Extraction incomplete | Run `fix_vosk_model.py` |
| **Low disk space** | No room for 1.4GB model | Free up 2GB disk space |

---

## Quick Fix (For Your Friend)

### Option 1: Quick Recovery
```bash
# Run this command in the project folder
python fix_vosk_model.py
```

**What it does:**
- ✓ Checks vosk package installation
- ✓ Downloads VOSK model (if missing/broken)
- ✓ Extracts and verifies
- ✓ Tests speech recognition
- ✓ Shows success message

Then run app again:
```bash
python app.py
# or
START.bat
```

---

### Option 2: Complete Reset
If `fix_vosk_model.py` doesn't work:

```powershell
# Delete broken model
Remove-Item vosk_model -Recurse -Force

# Re-run setup
python fix_vosk_model.py
```

---

### Option 3: Manual Re-setup
```bash
# Step 1: Delete everything
Remove-Item vosk_model -Recurse -Force
Remove-Item -Path *.zip -Filter "*vosk*" -Force

# Step 2: Reinstall packages
pip install --upgrade vosk

# Step 3: Download model
python download_vosk_model.py

# Step 4: Verify
python fix_vosk_model.py --verify-only

# Step 5: Run app
python app.py
```

---

## Troubleshooting Steps

### Check 1: Is vosk installed?
```bash
pip show vosk
```

If not:
```bash
pip install vosk
```

### Check 2: Does vosk_model exist?
```bash
dir vosk_model
```

Should show these folders:
```
vosk_model/
  ├─ am-english/
  ├─ conf/
  ├─ ctc.fst
  ├─ graph/
  ├─ ivector/
  ├─ model-am/
  └─ model-am.d/
```

If not, download:
```bash
python download_vosk_model.py
```

### Check 3: Test VOSK directly
```bash
python
>>> from vosk import Model, KaldiRecognizer
>>> model = Model("vosk_model")
>>> rec = KaldiRecognizer(model, 16000)
>>> print("VOSK works!")
```

If error → Run `python fix_vosk_model.py`

---

## Internet Connection Issues

If download keeps failing:

**Method 1: Faster Download URL**
```bash
# Download manually from browser, then do:
python download_vosk_model.py
# It will detect the ZIP and extract it
```

**Method 2: Use a different network**
- Try hotspot from phone
- Try colleague's network
- Try coffee shop WiFi

**Method 3: Download in parts**
```bash
# Download smaller chunks
pip install --upgrade pip
python fix_vosk_model.py  # Automatically restarts if interrupted
```

---

## Disk Space Issues

Check free space:
```bash
# Windows
dir C:\
# Shows "Available"
```

Need at least **2 GB free**.

cleanup:
```bash
# Delete temp files
del %TEMP%\*vosk*
del %TEMP%\*.zip

# Empty recycle bin
```

---

## Memory Issues

If getting "Not enough memory" error:

```bash
# Close these applications:
# - Chrome browser
# - Discord
# - Spotify
# - Any games running
# - Unnecessary background apps

# Then run:
python fix_vosk_model.py
```

Or increase virtual memory (Windows):
1. Right-click **This PC** → Properties
2. Click **Advanced system settings**
3. Click **Environment Variables**
4. See available disk... close unnecessary programs

---

## Last Resort - Complete Uninstall/Reinstall

```bash
# Remove everything
pip uninstall vosk -y
Remove-Item vosk_model -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item venv -Recurse -Force -ErrorAction SilentlyContinue

# Fresh install
pip install vosk numpy scipy scikit-learn librosa pyttsx3 sounddevice PyAudio

# Download model
python download_vosk_model.py

# Verify
python fix_vosk_model.py

# Run
python app.py
```

---

## When All Else Fails

1. **Restart computer** (clears memory/locks)
   ```
   Shutdown /r /t 0
   ```

2. **Check internet connection**
   ```
   ping google.com
   ```

3. **Update Windows** (might fix audio/driver issues)
   - Settings → Update & Security → Check for updates

4. **Try on different device** (confirms if problem is hardware)

5. **Contact support**
   - Share entire console output from `fix_vosk_model.py`
   - Mention: Windows version, Python version, disk space

---

## Files Provided

| File | Purpose |
|------|---------|
| `START.bat` | Enhanced - now auto-checks VOSK |
| `fix_vosk_model.py` | **NEW - Recovery tool** |
| `download_vosk_model.py` | Original downloader |

---

## Expected Success Signs

✓ After `fix_vosk_model.py` completes:
```
[SUCCESS] VOSK model ready!
=============================================================

You can now:
  1. Run: python app.py
  2. Or run: START.bat

Authentication and commands should work now!
```

✓ App launches and **Registration Window** appears
✓ Can register a new user with voice
✓ Can authenticate by speaking your name
✓ Can give voice commands (e.g., "open calculator")

---

## Need Help?

If stuck:
1. Run: `python diagnose_system.py` → Share output
2. Run: `python fix_vosk_model.py` → Share output
3. Check: `logs/app.log` for detailed errors  
4. Contact with screenshot of error message
