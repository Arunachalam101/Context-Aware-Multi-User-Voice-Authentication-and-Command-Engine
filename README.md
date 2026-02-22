# 🎤 Context-Aware Multi-User Voice Authentication and Command Engine

An **offline, fully-functional** voice authentication and command execution system built entirely in Python. No cloud services, no internet required.

## ✨ Features

✅ **Completely Offline** - Uses local models and databases  
✅ **Multi-User Support** - Authenticate multiple users by voice  
✅ **Speaker Recognition** - SVM/Random Forest ML models  
✅ **Voice Commands** - Execute system commands by voice  
✅ **Text-to-Speech** - Offline TTS with pyttsx3  
✅ **Speech Recognition** - Offline STT with VOSK  
✅ **SQLite Database** - Local data storage  
✅ **Modern GUI** - Tkinter-based user interface  
✅ **Modular Architecture** - Clean, independent modules  

## 📋 System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Microphone**: Working audio input device
- **Disk Space**: 2GB for VOSK model + additional space for features/models

## 🚀 Quick Start

### 1. Clone/Download Project
```bash
cd Context-Aware-Multi-User-Voice-Authentication-and-Command-Engine
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download VOSK Model
1. Visit: https://alphacephei.com/vosk/models
2. Download: `vosk-model-en-us-0.42-gigaspeech.zip` (recommended, ~1.4GB)
3. Extract to project root as `vosk_model/` directory

**Example:**
```
vosk_model/
├── am/
├── conf/
├── graph/
├── ivector/
└── ...
```

### 5. Run Application
```bash
python app.py
```

## 📚 Project Structure

```
├── app.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── audio/                          # Audio recording & processing
│   ├── recorder.py                 # Microphone recording
│   └── audio_utils.py              # Audio utilities
│
├── features/
│   └── mfcc_extractor.py           # MFCC feature extraction
│
├── database/                       # Database operations
│   ├── db_connection.py            # SQLite connection & schema
│   └── db_operations.py            # User/feature/log operations
│
├── ml/                             # Machine learning
│   ├── train_model.py              # Model training (SVM/RandomForest)
│   ├── model_loader.py             # Load pre-trained models
│   └── predict_speaker.py          # Speaker authentication
│
├── speech/
│   └── vosk_recognizer.py          # Offline speech-to-text
│
├── commands/                       # Command processing
│   ├── command_interpreter.py      # Map text to commands
│   └── action_executor.py          # Execute system actions
│
├── response/
│   └── tts_engine.py               # Text-to-speech engine
│
├── gui/                            # User interface
│   ├── main_ui.py                  # Main control panel
│   ├── register_ui.py              # User registration
│   └── auth_ui.py                  # Authentication & commands
│
├── utils/
│   └── config.py                   # Configuration & paths
│
├── data/                           # Data storage
│   ├── raw_audio/                  # Raw voice samples
│   └── processed_features/         # Extracted features
│
├── database/
│   └── voice_auth.db               # SQLite database
│
├── models/                         # ML models
│   ├── speaker_model.pkl           # Trained classifier
│   ├── feature_scaler.pkl          # Feature normalizer
│   └── metadata.pkl                # Model metadata
│
├── logs/                           # Application logs
│   └── app.log                     # Debug log
│
└── vosk_model/                     # VOSK speech model (download separately)
    └── [model files]
```

## 🔄 Workflow

### 1. User Registration
1. Launch application → Click "Register New User"
2. Enter username
3. Click "Record Sample" (minimum 3 samples required)
4. Record 3-second voice samples
5. MFCC features extracted automatically
6. Features stored in database

### 2. Train ML Model
1. Click "Train Speaker Model"
2. System loads all stored features
3. Trains SVM or Random Forest classifier
4. Saves model + scaler to `models/` directory
5. Ready for authentication

### 3. Authentication & Commands
1. Click "Authenticate & Command"
2. Record voice for authentication
3. System authenticates speaker
4. If authenticated, listen for voice command
5. Recognize command text with VOSK
6. Execute command (open notepad, calculator, tell time, etc.)
7. Speak response with TTS

## 🎯 Predefined Commands

The system recognizes these voice commands:

| Command | Action |
|---------|--------|
| "open notepad" | Opens text editor |
| "open calculator" | Opens calculator app |
| "open cmd" | Opens command prompt |
| "tell time" | Speaks current time |
| "system info" | Shows system information |
| "open file explorer" | Opens file manager |

**Easy to extend:** Add new commands in `utils/config.py` → `COMMANDS` dictionary

## 🧠 Machine Learning

### Training Algorithm Options:
1. **SVM (Support Vector Machine)** - Default
   - Kernel: RBF, Linear, or Polynomial
   - Better for smaller datasets
   - Fast inference

2. **Random Forest**
   - Ensemble of decision trees
   - Good for complex patterns
   - More robust

### Feature Extraction:
- **13 MFCC coefficients** (Mel-Frequency Cepstral Coefficients)
- **Statistics**: Mean and standard deviation
- **Total features**: 26-dimensional vectors
- **Normalization**: StandardScaler (zero mean, unit variance)

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Voice Features Table
```sql
CREATE TABLE voice_features (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    feature_vector BLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Command Logs Table
```sql
CREATE TABLE command_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    command TEXT,
    status TEXT DEFAULT 'executed',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## ⚙️ Configuration

Edit `utils/config.py` to customize:

- **Audio**: Sample rate, duration, channels
- **MFCC**: Number of coefficients, FFT settings
- **ML Model**: SVM kernel, Random Forest parameters
- **TTS**: Speech rate, volume, voice selection
- **Authentication Threshold**: Confidence cutoff for acceptance
- **Commands**: Add/remove voice commands

## 🔧 Troubleshooting

### VOSK Model Not Found
```
Download from: https://alphacephei.com/vosk/models
Extract to: vosk_model/ directory in project root
```

### No Microphone Detected
```
Check:
1. Audio device is connected and enabled
2. Permissions are granted to Python
3. No other app is exclusive to microphone
```

### Module Import Errors
```bash
pip install --upgrade -r requirements.txt
```

### Database Errors
```
Delete: database/voice_auth.db
Restart application (recreates schema automatically)
```

## 📝 Development Notes

### Module Independence
Each module can be tested independently:
```bash
python audio/recorder.py
python features/mfcc_extractor.py
python ml/train_model.py
python speech/vosk_recognizer.py
# etc.
```

### Adding New Features
1. Create module in appropriate directory
2. Use configuration from `utils/config.py`
3. Add database operations if needed
4. Update main UI if user-facing

### Extending Commands
```python
# In utils/config.py
COMMANDS = {
    # ... existing commands ...
    "your custom command": "action_name",
}

# In commands/action_executor.py
def execute_action(self, action_name, parameters=None):
    # ... existing actions ...
    elif action_name == "action_name":
        return self.your_custom_action()
```

## 📊 Performance Tips

- **Faster authentication**: Fewer MFCC coefficients (8-10)
- **Better accuracy**: More MFCC coefficients (13-20)
- **Faster training**: Fewer voice samples per user (3-5)
- **Better training**: More samples (10-20)

## 🔐 Security Notes

- Passwords NOT used (voice is the password)
- Feature vectors stored locally (not sent anywhere)
- Models saved in plaintext pickle format (consider encryption for production)
- Database access without authentication (local only)

## 📄 License

This project is provided as-is for educational and personal use.

## 🙏 Credits & Dependencies

- **librosa**: Audio feature extraction
- **scikit-learn**: Machine learning
- **VOSK**: Offline speech recognition
- **pyttsx3**: Text-to-speech
- **sounddevice**: Audio recording
- **tkinter**: GUI framework

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review module docstrings
3. Run individual modules for testing
4. Check logs in `logs/app.log`

---

**Built with ❤️ for offline voice authentication**

Last Updated: February 20, 2026
Version: 1.0.0
