# For Your Friend - How to Setup & Run

## Quick Start (3 Steps)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Arunachalam101/Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine.git
cd Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine
```

### Step 2: Run the Startup Script
```bash
START.bat
```

**What happens automatically:**
- ✓ Checks Python installation
- ✓ Installs all dependencies from requirements.txt
- ✓ Loads pre-trained models (included in repo)
- ✓ Downloads VOSK model (~1.4 GB, first time only)
- ✓ Launches the application

### Step 3: Enjoy!
```
Registration Window → Record your voice 3x
Authentication Window → Speak to login
Command Window → Give voice commands
```

---

## What's Included Now

✅ **Pre-trained ML Models** (4.3 KB)
- `speaker_model.pkl` - Speaker authentication
- `feature_scaler.pkl` - Audio feature scaling
- `metadata.pkl` - Model configuration

✅ **All Source Code** (19 Python modules)
- Speech recognition, voice authentication, command execution

✅ **Documentation** (17 guides)
- README.md, QUICK_START.md, deployment guides

✅ **Scripts**
- START.bat, START.ps1, setup helpers, diagnostics

---

## System Requirements

- **Python**: 3.8+ (auto-checks)
- **OS**: Windows (START.bat), Mac/Linux (use python app.py)
- **Internet**: Needed for first-run VOSK download (~5-15 mins)
- **Microphone**: For voice input
- **Disk Space**: ~2 GB free (for VOSK model)

---

## Troubleshooting

### "Python not found"
→ Install Python from python.org (ADD TO PATH during setup)

### "Module not found"
→ START.bat didn't complete. Run: `pip install -r requirements.txt`

### "Microphone not working"
→ Run: `python diagnose_system.py`
→ Check Windows Settings → Privacy → Microphone permissions

### "Speech recognition not working"
→ Check internet (needed for VOSK download)
→ Run: `python test_microphone.py`

---

## Features Ready to Use

✅ **User Registration** - Create account with voice biometrics
✅ **Voice Authentication** - Login by speaking your name
✅ **Speech Recognition** - Understands English commands
✅ **Voice Commands** - Execute actions (open apps, etc.)
✅ **Text-to-Speech** - System responds with voice feedback
✅ **Multi-user** - Different users, different voices
✅ **Offline** - Works completely offline after VOSK downloads

---

## For Developers

**If you want to modify/train:**
```bash
# See available training data
python ml/train_model.py

# Check audio/MFCC extraction
python features/mfcc_extractor.py

# Add new users
# Use GUI Registration Window
```

---

## Questions? Check These Files

- `README.md` - Project overview
- `QUICK_START.md` - Quick start guide
- `CLIENT_QUICK_START.md` - Client deployment
- `SPEECH_RECOGNITION_GUIDE.md` - Speech recognition setup
- `DEVICE_RESTART_FIX.md` - Troubleshooting memory issues

---

**Ready? Just run START.bat and enjoy!** 🚀
