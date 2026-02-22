# "Failed to create a model" Error - Fix Guide

## The Error Your Friend is Getting

```
VoskRecognitionError: Failed to initialize VOSK: Initialization error: Failed to create a model
[WARNING] VOSK recognizer failed to load
```

---

## What This Means

The VOSK speech recognition **model is corrupted or incomplete**.

| Likely Cause | Solution |
|------|----------|
| Model download was **incomplete** | Re-download |
| Model extraction **failed** | Re-extract |
| Model files **corrupted** | Delete and re-download |
| Missing critical model files | Run diagnostic |

---

## Quick Fix (2 Commands)

### Step 1: Diagnose the Problem
```bash
python diagnose_vosk.py
```

**This shows:**
- ✓ Which model files are present
- ✓ Which files are missing
- ✓ What the actual error is

### Step 2: Fix It
```bash
python fix_vosk_model.py
```

**This:**
- Deletes the broken model
- Re-downloads VOSK model
- Re-extracts completely
- Verifies all files are present
- Tests the model

---

## After Running Both Commands

```bash
START.bat
# or
python app.py
```

Should work now!

---

## If It Still Doesn't Work

### Complete Reset

```powershell
# Step 1: Delete broken model
Remove-Item vosk_model -Recurse -Force -ErrorAction SilentlyContinue

# Step 2: Delete any partial downloads
Remove-Item -Path *.zip -Filter "*vosk*" -Force -ErrorAction SilentlyContinue

# Step 3: Clear Python cache
Remove-Item __pycache__ -Recurse -Force -ErrorAction SilentlyContinue

# Step 4: Reinstall packages
pip install --force-reinstall vosk

# Step 5: Download fresh model
python download_vosk_model.py

# Step 6: Verify
python diagnose_vosk.py

# Step 7: Try running
python app.py
```

---

## What "Diagnose" Command Shows

Output should look like:

```
[1/4] Checking model structure...

  Model path: D:\...\vosk_model
  Model exists: True
  Model size: 3.75 GB

  ✓ am-english/              <- Should see check marks
  ✓ conf/
  ✓ graph/
  ✓ ivector/

  ✓ am-english/final.mdl     <- And for files
  ✓ conf/mfcc.conf
  ✓ graph/HCLG.fst
  ...

[2/4] Checking file permissions...
  ✓ Can read: conf\mfcc.conf
  ✓ Can read: graph\HCLG.fst

[3/4] Checking VOSK library...
  ✓ vosk.Model imported successfully
  ✓ Model loaded successfully!
  ✓ Recognizer created successfully!

DIAGNOSTIC SUMMARY
  Model structure: ✓ OK
  File permissions: ✓ OK
  VOSK library: ✓ OK

[SUCCESS] Model is ready to use!
```

---

## If Diagnose Shows Missing Files

Example output:
```
[1/4] Checking model structure...
  ✗ am-english/
  ✗ graph/
  
  [PROBLEM] Missing directories: ['am-english', 'graph']
  This means the model extraction was INCOMPLETE
  Solution: Delete and re-download the model
```

**Then run:**
```bash
python fix_vosk_model.py
```

---

## Internet Speed Issues

If download is slow:

**Check internet:**
```powershell
ping google.com
```

**Try with proxy/VPN:**
```bash
python fix_vosk_model.py
# The script will retry downloads automatically
```

**Or manually download:**
1. Open browser
2. Go to: https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip
3. Save to project folder as `vosk-model-en-us-0.42-gigaspeech.zip`
4. Then run: `python download_vosk_model.py` (it will detect and extract)

---

## Disk Space Check

Model needs **2 GB free**:

```powershell
# Check free space
Get-Volume C: | Select-Object SizeRemaining
```

If low:
1. Delete temp files: `Remove-Item $env:TEMP\* -Force -ErrorAction SilentlyContinue`
2. Empty recycle bin (Shift+Delete)
3. Uninstall unused programs
4. Move downloads/documents to external drive

---

## Files Provided

| File | Use When |
|------|----------|
| `diagnose_vosk.py` | **First** - See what's wrong |
| `fix_vosk_model.py` | **Second** - Fix the problem |
| `download_vosk_model.py` | Alternative if fix doesn't work |

---

## Success Criteria

After running these steps, your friend should see:

✅ `diagnose_vosk.py` shows: `[SUCCESS] Model is ready to use!`

✅ `python app.py` launches the GUI

✅ Registration window appears

✅ Can record voice samples

✅ Can authenticate by speaking

✅ Voice commands work

---

## Still Having Issues?

1. **Run diagnose first:** `python diagnose_vosk.py`
2. **Share the output** with error details
3. **Check:** Model path correct in config.py?
4. **Try:** Different network (hotspot, workplace WiFi)
5. **Last resort:** Delete everything and fresh install

---

## Q&A

**Q: How big is the model?**  
A: ~3.7 GB extracted, ~1.4 GB download

**Q: Why did it fail?**  
A: Network interrupted, disk full, or permission issues

**Q: How long does re-download take?**  
A: 5-30 minutes depending on internet speed

**Q: Do I need to download every time?**  
A: No! Only the first time. It's cached locally.

**Q: What if I delete vosk_model folder?**  
A: You can re-download anytime with `python download_vosk_model.py`

**Q: Can I use online speech recognition instead?**  
A: No, this system is offline-only for privacy
