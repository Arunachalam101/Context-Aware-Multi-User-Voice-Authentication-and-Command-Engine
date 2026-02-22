# Complete Setup Guide - Clone from GitHub to Running

This guide is for your friend who is cloning the Voice Authentication System from GitHub for the first time.

---

## **Step 1: Clone the Repository**

Open Command Prompt or PowerShell and run:

```bash
git clone https://github.com/Arunachalam101/Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine.git
cd Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine
```

**Expected output:**
```
Cloning into 'Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine'...
remote: Enumerating objects: 200, done.
...
Receiving objects: 100% (200/200), done.
```

---

## **Step 2: Check What's in the Folder**

After cloning, you should see:

```
Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine/
├── RUN.bat              ← Main launcher
├── INSTALL_OFFLINE.bat  ← For offline networks
├── app.py               ← Application
├── requirements.txt     ← Package list
├── offline_packages/    ← Pre-downloaded packages (if included)
├── models/              ← Pre-trained ML models
├── [source code folders]
├── CLIENT_START_HERE.md ← Simple user guide
└── [other files]
```

---

## **Step 3: Run One Command - Choose Your Method**

### **Option A: Online Installation (RECOMMENDED)**

If you have internet connection:

```bash
RUN.bat
```

**What happens:**
1. ✓ Checks Python is installed
2. ✓ Installs packages (vosk, numpy, scipy, etc.)
3. ✓ Downloads VOSK model (~1.4 GB, one-time)
4. ✓ Launches the app GUI automatically

**Time:** 5-10 minutes

### **Option B: Offline Installation**

If you have no internet or RUN.bat fails:

```bash
INSTALL_OFFLINE.bat
```

Then:

```bash
RUN.bat
```

**What happens:**
1. ✓ Installs from offline_packages folder (no internet needed)
2. ✓ Launches the app GUI automatically

**Time:** 2-3 minutes (offline) + 1 minute for VOSK setup

---

## **Step 4: What You Should See**

### **During Installation:**

```
Windows PowerShell
[*] Checking Python installation...
✓ Python 3.9.x detected
[*] Installing packages...
  Installing vosk        ████████░░ 80%
  Installing numpy       ██████████ 100%
  Installing scipy       ██████████ 100%
  [... more packages ...]
[*] Downloading VOSK model...
  vosk-model (1.4 GB)   ████████░░ 50%
[*] Starting Voice Authentication System...
```

### **Success - GUI Window Opens:**

```
┌─────────────────────────────────────┐
│ Voice Authentication System         │
│                                     │
│  [ Register New User ]              │
│  [ Authenticate User  ]             │
│  [ Run Voice Commands ]             │
│                                     │
└─────────────────────────────────────┘
```

---

## **Step 5: First Time Use**

### **A. Register a User**

1. Click: **"Register New User"**
2. Enter username (e.g., "John")
3. Click: **"Record Voice Sample"**
4. Speak clearly: "This is my voice. I am John."
5. Wait for completion
6. Click "Done"

### **B. Authenticate (Login)**

1. Click: **"Authenticate User"**
2. Choose user from list
3. Click: **"Start Authentication"**
4. Speak the phrase it asks
5. Result: "✓ Authentication Successful" or "✗ Try Again"

### **C. Run Voice Commands**

1. Click: **"Run Voice Commands"**
2. Start by saying: "Open command menu"
3. Say commands like:
   - "What time is it?"
   - "Tell me a joke"
   - "Show CPU usage"
   - etc.

---

## **Troubleshooting**

### **Problem: "Python not recognized"**

Your friend needs to install Python:

1. Download from: https://www.python.org/downloads/
2. Install (make sure to check "Add Python to PATH")
3. Restart computer
4. Run RUN.bat again

### **Problem: "Failed to download packages"**

Network issue:

```bash
# Option 1: Try again with longer timeout
pip install --default-timeout=1000 vosk

# Option 2: Use offline packages
INSTALL_OFFLINE.bat

# Option 3: Disable VPN/proxy temporarily and try again
```

### **Problem: "Failed to create a model" (VOSK error)**

Model issue:

```bash
# Run diagnostic
python diagnose_vosk.py

# Then auto-fix
python fix_vosk_model.py
```

Or your friend can read: **RUN_BAT_TROUBLESHOOTING.md**

### **Problem: "No microphone detected"**

```bash
# Test microphone
python test_microphone.py

# If it doesn't work:
# - Check microphone is connected
# - Check Windows Settings → Sound → Input device
# - Try a different USB microphone
```

---

## **Quick Checklist**

- [ ] Cloned from GitHub
- [ ] Double-clicked RUN.bat (or INSTALL_OFFLINE.bat)
- [ ] Application GUI opened
- [ ] Registered at least one user
- [ ] Successfully authenticated
- [ ] System is working ✓

---

## **What Works Out of the Box**

After installation, your friend can:

✅ **Register** voice profiles  
✅ **Authenticate** using voice (speaker verification)  
✅ **Execute** voice commands  
✅ **Manage** multiple users  
✅ **View** detailed logs and reports  
✅ **Use offline** (no internet needed for running)  
✅ **Run on Windows** (10/11)  

---

## **Files for Reference**

If your friend needs help:

| If they... | Read this file |
|-----------|---------------|
| Are confused | CLIENT_START_HERE.md |
| Got an error | RUN_BAT_TROUBLESHOOTING.md |
| Have network issues | NETWORK_INSTALLATION_GUIDE.md |
| Want to understand everything | OFFLINE_INSTALLATION_DEVELOPER_GUIDE.md |
| Need to manually install packages | requirements.txt + QUICK_REFERENCE.md |

---

## **Just Got It Working?**

Congratulations! 🎉

Next steps your friend can try:

1. **Register multiple users:**
   - Click "Register New User" multiple times
   - Each user has unique voice pattern

2. **Test commands:**
   - "What time is it?"
   - "Tell me a joke"
   - "Show system info"
   - "How much disk space do I have?"

3. **Check the database:**
   - Look at `database/voice_auth.db` in file explorer
   - View stored voice features and authentication logs

4. **Read the guide:**
   - Open `CLIENT_START_HERE.md` for detailed information

---

## **Contact for Help**

If something still doesn't work:

1. Run: `python diagnose_vosk.py`
2. Take screenshot of output
3. Take screenshot of error message
4. Share with project owner

**Key info to share:**
- Python version: `python --version`
- Installed packages: `pip list | grep vosk`
- Error message (full text)
- What your friend was doing when error happened

---

## **TL;DR - Absolute Shortest Version**

```bash
# 1. Clone
git clone https://github.com/Arunachalam101/Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine.git
cd Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine

# 2. Run
RUN.bat

# 3. Done! App opens.
```

---

## **FAQ for Your Friend**

**Q: Do I need internet?**  
A: Only for first-time setup to download packages and VOSK model. After that, it works offline.

**Q: What if RUN.bat doesn't work?**  
A: Try INSTALL_OFFLINE.bat, or check RUN_BAT_TROUBLESHOOTING.md

**Q: Can I use it without a microphone?**  
A: Yes, for testing. But voice features won't work without microphone.

**Q: How do I update the code?**  
A: `git pull` from the project folder

**Q: Is it safe to delete offline_packages?**  
A: Yes, but you'll need internet to run RUN.bat next time.

**Q: Where is my voice data stored?**  
A: `database/voice_auth.db` - SQLite database, local machine only.

---

## **Success Indicators**

Your friend will know it's working when:

✓ RUN.bat doesn't show errors  
✓ GUI window opens automatically  
✓ Can register a user  
✓ Can authenticate successfully  
✓ Can run voice commands  
✓ Microphone captures audio  
✓ System responds to voice  

---

## **Next: Tell Your Friend**

Share this message with your friend:

---

**Hi! Here's how to set up the Voice Authentication System:**

1. **Clone the GitHub repository:**
   ```bash
   git clone https://github.com/Arunachalam101/Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine.git
   cd Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine
   ```

2. **Run the application:**
   ```bash
   RUN.bat
   ```

3. **Wait 5-10 minutes** for first-time setup (packages + VOSK model download)

4. **The app opens automatically** - Register a user and test!

If RUN.bat fails, try `INSTALL_OFFLINE.bat` instead.

Having issues? Read `CLIENT_START_HERE.md` or `RUN_BAT_TROUBLESHOOTING.md`

That's it! 🎉

---

