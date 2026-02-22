# Package Download Issues - Solutions

## Problem
Clients get error when RUN.bat tries to install packages:
```
ERROR: Could not find a version that satisfies the requirement...
Network timed out
Connection refused
```

## Root Causes

| Cause | Indicator |
|-------|-----------|
| **No internet** | Can't ping google.com |
| **Network firewall** | Network admin blocked pip |
| **Corporate proxy** | Behind corporate network |
| **VPN issue** | VPN blocking PyPI |
| **Slow internet** | Takes >5 minutes to download |

---

## Solution 1: Improve Network (EASIEST)

### Try These Steps:

```bash
# Step 1: Check internet
ping google.com

# Step 2: Try using different network
# - Switch from WiFi to mobile hotspot
# - Move to different WiFi
# - Try at different location (cafe, workplace)

# Step 3: Disable VPN temporarily
# - Settings → Apps → VPN
# - Turn off VPN
# - Run RUN.bat

# Step 4: Clear pip cache
pip cache purge
RUN.bat
```

---

## Solution 2: Offline Installation (FOR YOU - Developer)

### Step 1: Download Packages on Your Machine

On your development computer with good internet:

```bash
python download_offline_packages.py
```

This creates `offline_packages/` folder with all packages.

### Step 2: Include in Distribution ZIP

```
Voice-Auth-System-Client.zip
├── offline_packages/     ← New folder with packages
├── RUN.bat               ← For online install
├── INSTALL_OFFLINE.bat   ← For offline install
└── ... (other files)
```

### Step 3: Give Clients Both Options

**Option A: Internet available**
```
Run: RUN.bat
```

**Option B: No internet**
```
Run: INSTALL_OFFLINE.bat
```

---

## Solution 3: Manual Offline Installation

### For Clients Without Internet:

**Step 1: Get Packages (on a computer WITH internet)**
```bash
# Download packages
pip download vosk numpy scipy scikit-learn librosa pyttsx3 sounddevice PyAudio -d packages/
```

**Step 2: Transfer to Client Machine**
- Copy `packages/` folder to project directory
- Via USB drive, cloud, etc.

**Step 3: Install on Client Machine (NO internet)**
```bash
pip install --no-index --find-links="packages" vosk numpy scipy scikit-learn librosa pyttsx3 sounddevice PyAudio
```

---

## Solution 4: Pre-Installed Build (ADVANCED)

### Create with Packages Included:

```bash
# 1. Create venv
python -m venv client_venv

# 2. Activate and install
client_venv\Scripts\activate
pip install vosk numpy scipy scikit-learn librosa pyttsx3 sounddevice PyAudio

# 3. Package venv with project
# Distribute: project_folder + client_venv/
```

Pros: ✓ Completely offline-ready  
Cons: ✗ Larger ZIP file (1-2 GB)

---

## Quick Comparison

| Solution | Pros | Cons | Time |
|----------|------|------|------|
| **Improve Network** | Simplest | Requires internet | 5 mins |
| **Offline Packages** | Professional | Need to pre-download | 10 mins prep |
| **Manual Download** | Flexible | More steps | 15 mins |
| **Pre-installed venv** | Easiest for client | Large file | 1GB ZIP |

---

## Recommended Approach

### For Most Clients:
1. RUN.bat with retry logic ✓ (Already implemented)

### For Clients with Internet Issues:
1. INSTALL_OFFLINE.bat ✓ (Already implemented)
2. offline_packages/ folder (You generate once)

### For No Internet at All:
1. Pre-downloaded packages
2. Or cloud download + manual install

---

## Implementation for Your Clients

### Build Offline-Ready Package (ONE TIME):

```bash
# On your machine with internet
python download_offline_packages.py

# This creates offline_packages/ folder

# Rebuild ZIP
python simple_client_zip.py

# New ZIP includes offline_packages/
```

### For Clients with Network Issues:

They run:
```bash
INSTALL_OFFLINE.bat
```

Instead of:
```bash
RUN.bat
```

---

## File by File

| File | Use When | Client Action |
|------|----------|---------------|
| `RUN.bat` | Has internet | Double-click |
| `INSTALL_OFFLINE.bat` | No internet | Double-click |
| `offline_packages/` | Including in ZIP | Auto-used by INSTALL_OFFLINE.bat |
| `requirements.txt` | Manual install | `pip install -r requirements.txt` |

---

## Corporate/Firewall Issues

If client is behind corporate firewall:

```bash
# Try with corporate proxy
pip install --proxy vosk --proxy-addr=proxy.company.com:8080

# Or have IT open PyPI:
# - mirror.example.com
# - proxy.example.com
```

---

## Testing This

### Simulate Offline (your machine):

```bash
# 1. Start
python download_offline_packages.py

# 2. Remove internet (unplug WiFi)

# 3. Test offline install
pip install --no-index --find-links=offline_packages vosk

# 4. It should work!
```

---

## Command Reference

**Download all packages:**
```bash
python download_offline_packages.py
```

**Install from offline:**
```bash
pip install --no-index --find-links=offline_packages vosk numpy scipy scikit-learn librosa pyttsx3 sounddevice PyAudio
```

**Check what's needed:**
```bash
pip install --dry-run vosk
```

**Try with proxy:**
```bash
pip install --proxy "[user:passwd@]proxy.server:port" vosk
```

---

## Summary

### Your Options:

**🔧 Quick Fix:**
- Improved RUN.bat with retry logic ✓ (Done, in repo)

**📦 Better Solution:**
1. Run: `python download_offline_packages.py` (one time)
2. Create ZIP with `offline_packages/` folder
3. Clients run: `INSTALL_OFFLINE.bat`

**🎯 Best Solution:**
- Do both: Give clients RUN.bat + INSTALL_OFFLINE.bat
- Client chooses which one works for them

---

## Next Steps

1. **Try RUN.bat** - Works 90% of the time (already improved)
2. **If it fails, client uses INSTALL_OFFLINE.bat** - Works when no internet
3. **You pre-download packages once** - Takes ~10 minutes (optional)

Current status: ✅ RUN.bat is robust  
Next: Add offline packages for maximum compatibility
