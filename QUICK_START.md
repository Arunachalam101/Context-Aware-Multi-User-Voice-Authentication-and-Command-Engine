# Quick Start Guide - Voice Authentication System

**All tests passing! ✅ System is ready to use.**

---

## Step 1: Download VOSK Model (Required for Speech Recognition)

The offline speech recognition requires a separate model file (~1.4GB).

1. Visit: https://alphacephei.com/vosk/models
2. Download: **vosk-model-en-us-0.42-gigaspeech.zip**
3. Extract the ZIP file
4. Copy the extracted folder to your project's root directory:
   ```
   d:\Context-Aware Multi-User Voice Authentication and Command Engine\vosk_model\
   ```

**Verify installation:**
```bash
# Should contain: mfcc.txt, am.txt, phones.txt, graph.fst, ivector_extractor.xml
ls vosk_model/
```

---

## Step 2: Launch the Application

```bash
cd "d:\Context-Aware Multi-User Voice Authentication and Command Engine"
python app.py
```

**Expected output:**
```
[OK] Application initialized successfully!
[GUI Window opens with Main control panel]
```

---

## Step 3: Register a New User

### Without Microphone (Quick Test):

1. Click **"📝 Register New User"** button
2. Enter username (e.g., `alice` or `john`)
3. Enter password
4. Click **"Start Recording"** button 3+ times
   - Each click simulates recording a voice sample
   - Progress bar shows samples collected (need ≥3)
5. Once ≥3 samples, click **"Complete Registration"**

### With Microphone (Real Audio):

1. Click **"📝 Register New User"** button
2. Enter username
3. Enter password
4. Click **"Start Recording"**
   - Hold microphone properly
   - Wait for 3-second recording to complete
   - Repeat 3+ times with different audio
5. Click **"Complete Registration"**
6. Save features to database automatically

---

## Step 4: Train Speaker Authentication Model

1. After registering 2+ users with samples each:
2. Click **"🧠 Train Speaker Model"** button
3. Wait for training (takes 3-5 seconds)
4. Status bar shows: **"✓ Model training completed successfully!"**
5. Model automatically saved to: `models/speaker_model.pkl`

**Training details:**
- Uses SVM classifier by default (see config.py to change to RandomForest)
- Requires ≥2 different speakers for training
- Creates feature scaling and label encoding

---

## Step 5: Test Authentication & Commands

1. Click **"🔐 Authenticate & Command"** button
2. **Phase 1: Speaker Authentication**
   - Click **"Start Recording"** 
   - Speak for 3 seconds (same voice as during registration)
   - System authenticates speaker
   - Status shows: `"✓ Authenticated as: [username]"`
3. **Phase 2: Command Execution**
   - Click **"Start Recording"** for command
   - Say one of these predefined commands:
     - "what is the time" → speaks current time
     - "tell me the time" → speaks current time
     - "open notepad" → opens Notepad
     - "open calculator" → opens Calculator
     - "open chrome" → opens web browser
     - "system info" → displays OS information
   - System recognizes command
   - Status shows: `"✓ Command executed: [command name]"`
   - System speaks the result back

---

## Step 6: View Registered Users

1. Click **"👥 View Registered Users"** button
2. See list of all registered speakers
3. Shows database statistics

---

## Step 7: Files Created by the System

After first run, your directory will contain:

```
project_root/
├── database/
│   └── voice_auth.db          ← SQLite database (users, features, logs)
├── data/
│   ├── raw_audio/              ← Recorded WAV files
│   └── processed_features/      ← Extracted MFCC features
├── models/
│   ├── speaker_model.pkl       ← Trained SVM/RF classifier
│   ├── scaler.pkl              ← Feature scaling transform
│   └── metadata.pkl            ← Model metadata
├── logs/                        ← Application logs (if enabled)
└── vosk_model/                  ← Speech recognition model
    └── (1.4GB model files)
```

---

## Predefined Commands & Actions

| Command Text | What Happens | Confidence Required |
|-------------|--------------|-------------------|
| "what is the time" | Speak current time | Any |
| "tell me the time" | Speak current time | Any |
| "open notepad" | Launch Notepad.exe | Any |
| "open calculator" | Launch Calculator | Any |
| "open chrome" | Open Chrome browser | Any |
| "system info" | Show OS details | Any |

**Add more commands:** Edit `utils/config.py` and add to `COMMANDS` dictionary.

---

## Troubleshooting

### Problem: "Vosk model not found"
**Solution:** Download and place model in `vosk_model/` directory

### Problem: "No audio device detected"
**Solution:** Check microphone is connected and working in Windows Sound settings

### Problem: "The number of classes has to be greater than one"
**Solution:** Register ≥2 different users before training model

### Problem: "Model files not found"
**Solution:** Train a new model first (button "🧠 Train Speaker Model")

### Problem: "Authentication failed"
**Solution:** 
- Use same voice as during registration
- Ensure clean audio without background noise
- Reduce authentication threshold in config.py if needed

### Problem: "Command not recognized"
**Solution:**
- System will suggest closest matches
- Try one of the predefined commands above
- Check for typos (fuzzy matching has 70% threshold)

---

## Performance Tips

1. **Better Recognition:** Speak clearly into microphone
2. **Better Authentication:** Register with natural speech (various tones)
3. **Faster Training:** More samples = better accuracy
4. **Cleaner Audio:** Reduce background noise during registration
5. **Faster Execution:** System runs locally (no internet delay)

---

## Architecture Overview

```
User Voice Input
    ↓
AudioRecorder (sounddevice)
    ↓
Audio Preprocessing (librosa)
    ↓
MFCC Feature Extraction (13 coefficients)
    ↓
Feature Vector (26 dimensions)
    ↓
├─→ Storage in SQLite Database
│
└─→ SVM Classifier Prediction
    ↓
Speaker ID + Confidence
    ↓
(If Authenticated)
    ↓
VoskRecognizer (offline speech-to-text)
    ↓
CommandInterpreter (fuzzy matching)
    ↓
ActionExecutor (system command)
    ↓
ResponseEngine (pyttsx3 TTS)
    ↓
Speak Result Back to User
```

---

## Configuration Options

Edit `utils/config.py` to customize:

```python
# Audio
SAMPLE_RATE = 16000          # Hz
AUDIO_DURATION = 3            # seconds
N_MFCC = 13                   # MFCC coefficients

# ML Model
ML_MODEL_TYPE = "svm"         # "svm" or "random_forest"
AUTHENTICATION_THRESHOLD = 0.7 # 0.0-1.0 confidence

# Commands
COMMAND_SIMILARITY_THRESHOLD = 0.7  # For fuzzy matching

# Paths (auto-generated)
DATABASE_FILE = ...
MODELS_DIR = ...
DATA_DIR = ...
```

---

## Keyboard Shortcuts (in GUI)

- **Escape:** Close current window
- **Ctrl+Q:** Quit application
- **Click Status Area:** Refresh display

---

## Testing Workflows

### Workflow 1: Basic Registration (No Audio)
```
1. Click "Register New User"
2. Enter username
3. Click "Start Recording" 3 times
4. Click "Complete Registration"
5. Database updated with 3 test features
```

### Workflow 2: Train Model
```
1. Register 2+ users (from Workflow 1)
2. Click "Train Speaker Model"
3. Wait for completion
4. Model saved to models/speaker_model.pkl
```

### Workflow 3: Full Authentication
```
1. Click "Authenticate & Command"
2. Record voice (same as registered user)
3. Wait for authentication
4. If success: Record command voice
5. System executes command
6. Result spoken back
```

### Workflow 4: View Statistics
```
1. Click "View Registered Users"
2. See registered speakers
3. Check database contents
```

---

## Next Steps (Recommended)

1. ✅ Download VOSK model
2. ✅ Run `python app.py`
3. ✅ Register 2 test users
4. ✅ Train model
5. ✅ Test authentication with microphone
6. ✅ Try voice commands
7. ✅ Experiment with different voices/accents
8. ✅ Fine-tune confidence threshold if needed

---

## Support Information

### Key Modules for Debugging
- `utils/config.py` - Settings
- `database/db_operations.py` - Data management
- `ml/train_model.py` - Model training logs
- `app.py` - Application initialization

### Logging
Logs are written to `logs/` directory if enabled in app.py

### Performance Metrics
All operations should complete in seconds:
- Recording: 3 seconds
- Feature extraction: <1 second
- Model training: <5 seconds
- Prediction: <100ms
- Speech recognition: Variable (depends on audio)

---

**System Status:** Production Ready ✅  
**Last Updated:** 2025-02-21  
**Deadline:** 2025-02-25
