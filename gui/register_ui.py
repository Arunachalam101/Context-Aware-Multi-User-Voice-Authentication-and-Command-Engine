"""
User registration GUI for Voice Authentication System.

Allows users to:
- Enter username
- Record multiple voice samples
- Save features to database
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pathlib import Path
import threading
import numpy as np

# Import modules
try:
    from audio.recorder import AudioRecorder, RecorderError
    from audio.audio_utils import validate_audio
    from features.mfcc_extractor import MFCCExtractor, MFCCExtractionError
    from database.db_operations import UserManager, VoiceFeatureManager
    from utils.config import AUDIO_DURATION, MIN_SAMPLES_FOR_TRAINING
except ImportError:
    print("Warning: Some modules not available in register_ui")


class RegisterWindow:
    """
    User registration window for collecting voice samples.

    Workflow:
    1. Enter username
    2. Record voice samples (minimum 3)
    3. Auto-extract features
    4. Save to database
    """

    def __init__(self, window):
        """
        Initialize registration window.

        Args:
            window: Tkinter window.
        """
        self.window = window
        self.window.title("Register New User")
        self.window.geometry("600x500")

        # Initialize managers
        try:
            self.user_manager = UserManager()
            self.feature_manager = VoiceFeatureManager()
            self.recorder = AudioRecorder(duration=AUDIO_DURATION)
            self.mfcc_extractor = MFCCExtractor()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize: {str(e)}")
            return

        # State variables
        self.username = None
        self.samples_collected = 0
        self.features_list = []
        self.is_recording = False

        # Setup UI
        self._create_widgets()

    def _safe_update(self, callback):
        """
        Safely update UI from background thread.
        Checks if window still exists before updating.
        
        Args:
            callback: Function to call if window exists.
        """
        def safe_callback():
            try:
                if self.window.winfo_exists():
                    callback()
            except:
                pass  # Window or widget no longer exists
        
        self.window.after(0, safe_callback)

    def _create_widgets(self):
        """Create registration window widgets."""

        # Header
        header = ttk.Label(
            self.window,
            text="👤 User Registration",
            font=("Segoe UI", 16, "bold"),
        )
        header.pack(pady=15)

        # Username frame
        username_frame = ttk.LabelFrame(self.window, text="Step 1: Enter Username", padding=15)
        username_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(username_frame, text="Username:").pack(anchor=tk.W)

        self.username_entry = ttk.Entry(username_frame, width=30, font=("Segoe UI", 11))
        self.username_entry.pack(anchor=tk.W, pady=5)

        self.start_btn = ttk.Button(
            username_frame,
            text="✓ Start Registration",
            command=self._on_start_registration,
        )
        self.start_btn.pack(anchor=tk.W, pady=5)

        # Recording frame
        record_frame = ttk.LabelFrame(
            self.window,
            text=f"Step 2: Record Voice Samples (minimum {MIN_SAMPLES_FOR_TRAINING})",
            padding=15,
        )
        record_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Status label
        self.status_var = tk.StringVar(value="Enter username to start")
        self.status_label = ttk.Label(
            record_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            foreground="blue",
        )
        self.status_label.pack(pady=10)

        # Sample counter
        self.counter_var = tk.StringVar(value="Samples: 0")
        self.counter_label = ttk.Label(
            record_frame,
            textvariable=self.counter_var,
            font=("Segoe UI", 10, "bold"),
        )
        self.counter_label.pack()

        # Record button
        self.record_btn = ttk.Button(
            record_frame,
            text="🎤 Record Sample",
            command=self._on_record,
            state=tk.DISABLED,
        )
        self.record_btn.pack(pady=15, fill=tk.X)

        # Progress bar
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            record_frame,
            variable=self.progress_var,
            maximum=100,
            mode="determinate",
        )
        self.progress_bar.pack(fill=tk.X, pady=10)

        # Info text
        info_text = tk.Text(record_frame, height=6, width=60, font=("Courier", 9))
        info_text.pack(fill=tk.BOTH, expand=True, pady=10)
        info_text.insert(tk.END, "Recording Instructions:\n\n")
        info_text.insert(tk.END, f"1. Click 'Record Sample' button\n")
        info_text.insert(tk.END, f"2. Speak clearly for {AUDIO_DURATION} seconds\n")
        info_text.insert(tk.END, f"3. Record at least {MIN_SAMPLES_FOR_TRAINING} samples\n")
        info_text.insert(tk.END, f"4. Samples are saved automatically\n")
        info_text.insert(tk.END, f"5. Click 'Complete' to finish\n")
        info_text.config(state=tk.DISABLED)

        # Buttons frame
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        self.complete_btn = ttk.Button(
            button_frame,
            text="✓ Complete Registration",
            command=self._on_complete,
            state=tk.DISABLED,
        )
        self.complete_btn.pack(side=tk.LEFT, padx=5)

        self.cancel_btn = ttk.Button(
            button_frame,
            text="✕ Cancel",
            command=self._on_cancel,
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=5)

    def _on_start_registration(self):
        """Handle start registration."""
        username = self.username_entry.get().strip()

        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return

        if " " in username:
            messagebox.showerror("Error", "Username cannot contain spaces")
            return

        # Check if username already exists
        if self.user_manager.user_exists(username):
            messagebox.showerror("Error", f"Username '{username}' already exists")
            return

        # Register user
        try:
            self.user_manager.register_user(username)
            self.username = username

            # Enable recording
            self.status_var.set(f"Ready to record samples for '{username}'")
            self.record_btn.config(state=tk.NORMAL)
            self.username_entry.config(state=tk.DISABLED)
            self.start_btn.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to register user: {str(e)}")

    def _on_record(self):
        """Handle record button."""
        if self.is_recording:
            messagebox.showwarning("Warning", "Already recording")
            return

        if not self.username:
            messagebox.showerror("Error", "Please start registration first")
            return

        self.is_recording = True
        self.record_btn.config(state=tk.DISABLED)
        self.status_var.set(f"🎤 Recording... Please speak for {AUDIO_DURATION} seconds")

        # Run recording in separate thread
        thread = threading.Thread(target=self._record_thread)
        thread.start()

    def _record_thread(self):
        """Record audio in background thread."""
        try:
            # Record audio
            audio = self.recorder.record(show_progress=False)

            if audio is None:
                self._safe_update(lambda: self.status_var.set("Recording cancelled"))
                self.is_recording = False
                self._safe_update(lambda: self.record_btn.config(state=tk.NORMAL))
                return

            # Validate audio
            is_valid, message = validate_audio(audio)
            if not is_valid:
                self._safe_update(lambda: messagebox.showwarning("Audio Validation", message))
                self.is_recording = False
                self._safe_update(lambda: self.record_btn.config(state=tk.NORMAL))
                return

            # Extract features
            self._safe_update(lambda: self.status_var.set("🔄 Extracting MFCC features..."))

            features = self.mfcc_extractor.get_feature_vector(audio, compute_stats=True)
            self.features_list.append(features)

            # Store in database
            self.feature_manager.store_feature(self.username, features)

            # Update counter
            self.samples_collected += 1
            sample_count = self.samples_collected
            self._safe_update(lambda: self.counter_var.set(f"Samples: {sample_count}"))

            # Update progress
            progress = min(100, (sample_count / MIN_SAMPLES_FOR_TRAINING) * 100)
            self._safe_update(lambda: self.progress_var.set(progress))

            # Update status
            if sample_count >= MIN_SAMPLES_FOR_TRAINING:
                self._safe_update(lambda: self.status_var.set(f"✓ Ready to complete! ({sample_count} samples)"))
                self._safe_update(lambda: self.complete_btn.config(state=tk.NORMAL))
            else:
                remaining = MIN_SAMPLES_FOR_TRAINING - sample_count
                self._safe_update(lambda: self.status_var.set(f"✓ Sample {sample_count} recorded! ({remaining} more needed)"))

            self._safe_update(lambda: messagebox.showinfo("Success", f"Sample {self.samples_collected} recorded successfully!"))

        except RecorderError as e:
            self._safe_update(lambda: messagebox.showerror("Recording Error", str(e)))
            self._safe_update(lambda: self.status_var.set("Recording failed"))

        except MFCCExtractionError as e:
            self._safe_update(lambda: messagebox.showerror("Feature Extraction Error", str(e)))
            self._safe_update(lambda: self.status_var.set("Feature extraction failed"))

        finally:
            self.is_recording = False
            self._safe_update(lambda: self.record_btn.config(state=tk.NORMAL))

    def _on_complete(self):
        """Handle complete registration."""
        if self.samples_collected < MIN_SAMPLES_FOR_TRAINING:
            messagebox.showerror(
                "Error",
                f"Need at least {MIN_SAMPLES_FOR_TRAINING} samples "
                f"({self.samples_collected} collected)"
            )
            return

        try:
            messagebox.showinfo(
                "Success",
                f"✓ User '{self.username}' registered with {self.samples_collected} samples!\n\n"
                "Next: Train the model using the main window."
            )
            self.window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to complete: {str(e)}")

    def _on_cancel(self):
        """Handle cancel button."""
        if self.username and self.samples_collected > 0:
            if not messagebox.askyesno("Cancel", "Discard registration?"):
                return

            # Delete user and features if any were recorded
            try:
                self.user_manager.delete_user(self.username)
            except:
                pass

        self.window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    RegisterWindow(root)
    root.mainloop()
