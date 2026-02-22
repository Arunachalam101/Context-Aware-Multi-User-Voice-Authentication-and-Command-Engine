# RUN.bat Troubleshooting Guide

## Error Messages & Solutions

### ❌ "Failed to download packages" / "ERROR: Could not find a version"

**Causes:**
- No internet connection
- Network firewall blocking PyPI
- PyPI server temporarily down
- VPN blocking package downloads

**Solutions:**

```powershell
# 1. Check internet first
ping google.com
# Success? Continue to step 2
# Failure? Fix internet and try again

# 2. Clear pip cache
pip cache purge

# 3. Try with longer timeout
pip install --default-timeout=1000 vosk

# 4. If still fails, use offline packages
INSTALL_OFFLINE.bat
```

---

### ❌ "python: command not found" / "Python not recognized"

**Causes:**
- Python not installed
- Python not in PATH
- Wrong Python version (need 3.8+)

**Solutions:**

```powershell
# Check Python is installed
python --version

# If shows Python 3.8+, it's working

# If not recognized:
# 1. Windows: Add Python to PATH (see below)
# 2. Restart computer
# 3. Run RUN.bat again

# Still not working?
# Manually install packages:
cd project_folder
py -3.9 -m pip install vosk numpy scipy scikit-learn librosa pyttsx3 sounddevice PyAudio
python app.py
```

---

### ❌ "Permission denied" / "Access denied"

**Causes:**
- Folder is read-only
- Antivirus blocking file access
- Insufficient permissions

**Solutions:**

```powershell
# 1. Check folder permissions (Windows)
# Right-click folder → Properties
# Security → Edit → Your name → Full Control ✓

# 2. Disable antivirus temporarily
# Temporarily turn off Windows Defender or 3rd party antivirus
# Run RUN.bat
# Re-enable antivirus

# 3. Run as Administrator
# Right-click RUN.bat → "Run as administrator"
```

---

### ❌ "VOSK model not found" / "Failed to initialize"

**Causes:**
- VOSK model didn't download completely
- Corrupted model files
- Wrong folder structure

**Solutions:**

```powershell
# Option 1: Let RUN.bat re-download
# Delete: models/vosk_model/
# Run: RUN.bat again

# Option 2: Manual model placement
mkdir models\vosk_model
# Download from: https://alphacephei.com/vosk/models
# Extract into: models/vosk_model/
# Should have: models/vosk_model/model/*, not models/vosk_model/vosk_model/...

# Option 3: Use recovery tool
python fix_vosk_model.py
```

---

### ❌ "ModuleNotFoundError: No module named 'vosk'"

**Causes:**
- Package installation failed but script continued
- Python can't find installed packages
- Wrong Python version

**Solutions:**

```powershell
# Check what's installed
pip list | find "vosk"

# If not found, try again
pip install --default-timeout=1000 vosk

# If still fails, use offline
python download_offline_packages.py
# Then: INSTALL_OFFLINE.bat

# If packages show in list but still error:
# 1. Restart computer
# 2. Run RUN.bat again
```

---

### ❌ "PyAudio installation failed"

**Causes:**
- C++ compiler missing (Windows)
- Audio drivers missing
- Python dev headers missing

**Solutions:**

```powershell
# On Windows, try:
pip install pipwin
pipwin install pyaudio

# If that fails, app can still work without it
# (Audio input may fail, but mock microphone works)

# Alternative: Don't install PyAudio, use sounddevice
pip install --default-timeout=1000 sounddevice
```

---

### ❌ Slow downloads / "timed out waiting"

**Causes:**
- Slow internet connection
- Overloaded PyPI mirror
- Network congestion

**Solutions:**

```powershell
# Already fixed in RUN.bat with --default-timeout=1000
# But if still slow:

# 1. Try different PyPI mirror
pip install -i https://mirrors.aliyun.com/pypi/simple/ vosk

# 2. Use offline packages instead
python download_offline_packages.py
INSTALL_OFFLINE.bat
```

---

## Step-by-Step Debugging

### When RUN.bat fails, follow this exactly:

```powershell
# Step 1: Get information
python --version              # Should show 3.8+
pip --version                 # Should show version
ping google.com              # Should show successful pings

# Step 2: Try manual install with verbose output
pip install --default-timeout=1000 -v vosk

# Take screenshot of error message

# Step 3: Try with specific package (find which one fails)
pip install vosk
pip install numpy
pip install scipy
pip install scikit-learn
pip install librosa
pip install pyttsx3
pip install sounddevice
pip install PyAudio

# Step 4: Which package fails?
# - vosk? → Model issue (internet needed, or download separately)
# - numpy? → Compiler issue (MinGW/Visual C++ needed)
# - PyAudio? → Audio libraries missing
# - others? → Network timeout

# Step 5: Fix that specific package
# See solutions above for each
```

---

## Is It a Network Issue?

### Quick check:

```powershell
# These should all work:
ping google.com              # ✓ Internet working?
python -m pip --version      # ✓ Pip working?
pip install --dry-run vosk   # ✓ Can pip reach PyPI?

# If any fail → Network issue
# Solutions: Use VPN, mobile hotspot, or offline packages
```

---

## Corporate/Proxy Network

If behind corporate network and RUN.bat fails:

```powershell
# Option 1: Use corporate proxy
pip install --proxy "[user:passwd@]proxy.company.com:port" vosk

# Option 2: Use offline packages (recommended)
# Get IT to approve offline installation
INSTALL_OFFLINE.bat

# Option 3: Ask IT to mirror packages
# Request IT support to mirror:
# - vosk
# - numpy
# - scipy
# - scikit-learn
# - librosa
# - pyttsx3
# - sounddevice
# - PyAudio
```

---

## When Everything Fails

### Last resort recovery:

```powershell
# 1. Fully clean install
rmdir /s /q venv
rmdir /s /q models\vosk_model
pip cache purge

# 2. Reinstall Python (if needed)
# Uninstall → Reinstall from python.org

# 3. Try offline packages
python download_offline_packages.py
INSTALL_OFFLINE.bat

# 4. Contact support
# Share output of:
python --version
pip --version
pip list
# Screenshot of error
```

---

## File-by-File Expected Output

### Successful RUN.bat should show:

```
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Checking Python installation...
Python 3.9.x (or higher) ✓
Gathering system information...
[Output about CPU, RAM, Disk]
Installing packages...
<Lots of text about downloading and installing>
...
Successfully installed vosk numpy scipy scikit-learn librosa pyttsx3 sounddevice PyAudio
Downloading VOSK model...
[Shows download progress]
Starting Voice Authentication System...
```

Then Tkinter window should appear.

---

## Common Messages Decoded

| Message | Means | Action |
|---------|-------|--------|
| `Retrying package installation...` | Failed once, trying again | Wait, should succeed |
| `WARNING: Some packages failed` | Installation issues | Use INSTALL_OFFLINE.bat |
| `Model download taking long time` | Big file, slow network | Let it run or use pre-downloaded |
| `Registration window already open` | App already running | Close first instance |
| `Could not initialize audio` | No microphone | Use headset or disable |

---

## Testing Your Fix

After trying a solution, verify it works:

```powershell
# Test 1: Packages installed?
pip list | find "vosk"    # Should show vosk version

# Test 2: Python can load packages?
python -c "import vosk; print('vosk OK')"

# Test 3: Model present?
dir models\vosk_model      # Should show folders

# Test 4: App can start?
python app.py              # Should open GUI

# All good? System is working! ✓
```

---

## Can't Find Your Issue?

### Get diagnostic info:

1. Run: `python diagnose_vosk.py`
2. Share output with support
3. Share screenshot of RUN.bat error

Provides:
- Python version
- Installed packages
- VOSK model status
- Audio device info
- Exact error messages

---

## Contact Support

If RUN.bat still fails after trying these:

1. Run: `python diagnose_vosk.py`
2. Take screenshot of full error
3. Share:
   - Error message (full text)
   - Your network type (home, corporate, school)
   - Your OS (Windows 10/11, version)
   - Python version (`python --version`)
   - Diagnostic output

---

## Summary: Troubleshooting Flow

```
RUN.bat fails?
│
├─ Python error? → Install Python 3.8+
├─ Package error? → Try INSTALL_OFFLINE.bat
├─ Network error? → Check internet, disable VPN
├─ Model error? → Run fix_vosk_model.py
├─ Permission error? → Run as Administrator
└─ Still broken? → Run diagnose_vosk.py & contact support
```
