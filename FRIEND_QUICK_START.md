# 🎙️ Voice Authentication System - Fresh Start Guide

**For:** Your friend cloning from GitHub for the first time  
**Time needed:** 20-30 minutes  
**Difficulty:** ⭐ Very Easy (just follow the steps)

---

## ✅ Step-by-Step Setup

### **Step 1: Clone the Repository** (2 minutes)

Open Command Prompt or PowerShell and run:

```bash
git clone https://github.com/Arunachalam101/Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine.git

cd Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine
```

Now you have all the code! ✓

---

### **Step 2: Check Python is Installed** (1 minute)

Run this command to verify:

```bash
python --version
```

**Expected output:** `Python 3.8` or higher (e.g., `Python 3.11.0`, `Python 3.13.0`)

**If Python is not found:**
- Download from: https://www.python.org/downloads/
- During installation: ✅ **Check "Add Python to PATH"**
- Restart Command Prompt
- Run `python --version` again

---

### **Step 3: Install Required Packages** (5 minutes)

Run this command to install all dependencies:

```bash
pip install -r requirements.txt
```

You'll see lots of text as packages download and install. Wait for it to finish. ✓

**If you get timeout errors:**
- Your internet is slow - no problem!
- Use the offline installation instead (see below)

---

### **Step 4: Download the VOSK Model** (10-20 minutes)

This is the speech recognition AI model (~1.4 GB). Run:

```bash
python download_vosk_model.py
```

Follow the prompts:
- It will ask: "Choose option [1/2]" 
- Type: `1` and press Enter
- The model will download automatically
- You'll see a progress bar like: `[████████████░░░░░░░░░░░░░] 50%`
- When done, it shows: `✓ VOSK MODEL SETUP COMPLETE!`

⏳ **This takes 10-30 minutes** depending on your internet speed.

---

### **Step 5: Verify Everything Works** (2 minutes)

Test the diagnostic tool:

```bash
python diagnose_vosk.py
```

You should see:
```
✓ Model structure: OK
✓ File permissions: OK  
✓ VOSK library: OK
```

If something shows ✗, run this fix:
```bash
python fix_vosk_model.py
```

---

### **Step 6: Launch the Application!** (1 minute)

Simply double-click or run:

```bash
python app.py
```

Or use the quick launcher:

```bash
.\RUN.bat
```

🎉 **The Voice Authentication System GUI will open!**

---

## 🚀 You're Done!

The app is now ready to use:

1. **Register** - Create a new user account with voice
2. **Authenticate** - Log in with your voice
3. **Commands** - Issue voice commands to the system
4. **Multi-user** - Add more users to the system

---

## ⚠️ Troubleshooting

### **Problem: "Python not found"**
```
❌ 'python' is not recognized as an internal or external command
```
**Solution:**
1. Install Python from https://www.python.org/
2. ✅ Check "Add Python to PATH" during installation
3. Restart your terminal
4. Try again

---

### **Problem: "pip install" fails with timeout**
```
❌ ERROR: Failed to download packages
```
**Solution 1 - Faster internet:**
```bash
pip install --default-timeout=1000 -r requirements.txt
```

**Solution 2 - Use offline packages** (if available):
```bash
# If offline_packages folder exists in your repo:
pip install --no-index --find-links=offline_packages -r requirements.txt
```

---

### **Problem: VOSK model download fails**
```
❌ Download failed / Connection timeout
```
**Solution:**
1. Run again (retry):
   ```bash
   python download_vosk_model.py
   ```

2. If it keeps failing, use manual download:
   - Go to: https://alphacephei.com/vosk/models/
   - Download: `vosk-model-en-us-0.42-gigaspeech.zip`
   - Extract to: `vosk_model` folder in your project
   - Run: `python app.py`

---

### **Problem: "Failed to create a model" error**
```
❌ VoskRecognitionError: Failed to create a model
```
**Solution:**
```bash
python fix_vosk_model.py
```
This auto-fixes model issues.

---

### **Problem: "ModuleNotFoundError: No module named vosk"**
```
❌ ModuleNotFoundError: No module named 'vosk'
```
**Solution:**
Packages didn't install correctly. Try again:
```bash
pip install vosk numpy scipy scikit-learn librosa pyttsx3 sounddevice PyAudio
```

---

## 📋 Quick Summary - 6 Commands

Your friend only needs to run these 6 commands in order:

```bash
# 1. Clone the repo
git clone https://github.com/Arunachalam101/Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine.git
cd Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine

# 2. Check Python
python --version

# 3. Install packages
pip install -r requirements.txt

# 4. Download VOSK model (choose option 1)
python download_vosk_model.py

# 5. Verify setup
python diagnose_vosk.py

# 6. Run the app!
python app.py
```

Done! 🎉

---

## 🎯 Expected Timeline

| Step | Task | Time |
|------|------|------|
| 1 | Git clone | 1-2 min |
| 2 | Check Python | 1 min |
| 3 | Install packages | 5 min |
| 4 | Download VOSK | 10-20 min ⏳ (slowest step) |
| 5 | Verify setup | 2 min |
| 6 | Run app | 1 min |
| **TOTAL** | **Complete setup** | **20-30 min** |

---

## ✨ What Happens When App Runs

A GUI window opens with:

1. **Home Screen**
   - Options: Register, Authenticate, Commands
   - Status display

2. **Register Screen**
   - Enter username
   - Click "Start Recording"
   - Speak your voice sample (3-5 sentences)
   - System saves your voice profile

3. **Authenticate Screen**
   - Click "Start Speaking"
   - Speak to log in
   - System verifies it's you
   
4. **Commands Screen**
   - Say commands like: "Open browser", "What time is it?"
   - System executes voice commands

---

## 📞 If Something Goes Wrong

1. **Run diagnostic:**
   ```bash
   python diagnose_vosk.py
   ```

2. **Read the relevant fix:**
   - `RUN_BAT_TROUBLESHOOTING.md` - Detailed error solutions
   - `FRIEND_SETUP.md` - Setup-specific help
   - `VOSK_INITIALIZATION_FIX.md` - Model-specific issues

3. **Still stuck?**
   - Check internet connection: `ping google.com`
   - Try running commands again (sometimes just works on retry)
   - Check you have 2GB free disk space

---

## 🎓 For Advanced Users

If you want to customize the system:

- **Models:** `ml/` folder - Contains speaker authentication models
- **Speech:** `speech/vosk_recognizer.py` - Speech recognition config
- **Commands:** `commands/command_interpreter.py` - Add custom voice commands
- **GUI:** `gui/` folder - Tkinter interface

---

## ✅ Checklist

Does your friend have everything for a fresh start?

- [ ] Git installed (or download ZIP from GitHub)
- [ ] Python 3.8+ installed with PATH added
- [ ] Internet connection (for downloads)
- [ ] ~2 GB free disk space
- [ ] 20-30 minutes of time

**Got all that?** They're ready to start! ✓

---

## 📚 Documentation

All these files are in the repo. Your friend can read them for more info:

- `CLIENT_START_HERE.md` - Simplest start guide
- `QUICK_START.md` - Quick overview
- `RUN_BAT_TROUBLESHOOTING.md` - Detailed error help
- `README.md` - Complete project info
- `FRIEND_SETUP.md` - Another friend setup guide

---

## 🚀 Summary for Your Friend

> Hi! To use this Voice Authentication System:
>
> 1. **Clone:** `git clone [repo-url]`
> 2. **Install Python** (if not already)
> 3. **Install packages:** `pip install -r requirements.txt`
> 4. **Download VOSK:** `python download_vosk_model.py`
> 5. **Run:** `python app.py`
>
> That's it! The app will open in ~20-30 minutes after step 1.
>
> If anything fails, run: `python diagnose_vosk.py`
>
> Questions? Check: `FRIEND_SETUP.md` or `RUN_BAT_TROUBLESHOOTING.md`

---

**Happy Voice Authentication! 🎙️**
