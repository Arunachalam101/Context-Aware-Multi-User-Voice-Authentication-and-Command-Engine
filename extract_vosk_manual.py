"""
Manual VOSK Model Extractor
Run this after downloading the ZIP manually
"""

import zipfile
import os
import shutil

def extract_vosk_model():
    zip_file = "vosk-model-en-us-0.42-gigaspeech.zip"
    extract_temp = "temp_vosk"
    final_dir = "vosk_model"
    
    print("🔧 Manual VOSK Model Setup")
    print("=" * 50)
    
    # Check if ZIP exists
    if not os.path.exists(zip_file):
        print(f"❌ ERROR: {zip_file} not found!")
        print(f"📥 Please download from: https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip")
        print(f"📂 Save it to: {os.getcwd()}")
        return False
    
    # Check ZIP size
    size_gb = os.path.getsize(zip_file) / 1024**3
    print(f"📦 ZIP file found: {size_gb:.2f} GB")
    
    if size_gb < 1.0:
        print("⚠️  WARNING: ZIP file seems small (should be ~1.4 GB)")
        print("   Download may be incomplete. Check file in browser.")
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            return False
    
    try:
        print("🗜️  Extracting ZIP file...")
        
        # Clean up old files
        if os.path.exists(final_dir):
            shutil.rmtree(final_dir)
        if os.path.exists(extract_temp):
            shutil.rmtree(extract_temp)
        
        # Extract ZIP
        with zipfile.ZipFile(zip_file, 'r') as z:
            z.extractall(extract_temp)
        
        print("✅ Extraction successful!")
        
        # Find the model folder
        items = os.listdir(extract_temp)
        print(f"📁 Found: {items}")
        
        model_folder = None
        for item in items:
            item_path = os.path.join(extract_temp, item)
            if os.path.isdir(item_path):
                model_folder = item_path
                break
        
        if model_folder:
            # Move to final location
            shutil.move(model_folder, final_dir)
            print(f"📂 Moved model to: {final_dir}/")
            
            # Clean up temp
            shutil.rmtree(extract_temp)
            
            # Verify contents
            model_files = os.listdir(final_dir)
            print(f"📋 Model contains {len(model_files)} files/folders:")
            for f in sorted(model_files)[:10]:  # Show first 10
                print(f"   - {f}")
            if len(model_files) > 10:
                print(f"   ... and {len(model_files)-10} more")
            
            # Check for required folders
            required = ['am', 'conf', 'graph', 'ivector']
            missing = []
            for req in required:
                if not any(req in f for f in model_files):
                    missing.append(req)
            
            if missing:
                print(f"⚠️  Missing folders: {missing}")
                print("   Model may not work correctly")
            else:
                print("✅ All required model components found!")
            
            print("\n🎉 VOSK model setup complete!")
            print("📝 Next step: Run 'python app.py' to test")
            return True
        else:
            print("❌ ERROR: No model folder found in ZIP")
            return False
            
    except zipfile.BadZipFile:
        print("❌ ERROR: ZIP file is corrupted")
        print("💡 Solution: Re-download the ZIP file")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = extract_vosk_model()
    if success:
        print("\n🚀 Ready to run: python app.py")
    else:
        print("\n❌ Setup failed. Please try again or use automatic downloader.")