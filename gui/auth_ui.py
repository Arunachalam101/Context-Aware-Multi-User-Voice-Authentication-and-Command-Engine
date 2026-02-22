"""
Authentication GUI for Voice Authentication System.

Handles:
- Voice authentication
- Voice command execution
- Results display
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import threading
import numpy as np

# Import modules
try:
    from audio.recorder import AudioRecorder, RecorderError
    from features.mfcc_extractor import MFCCExtractor, MFCCExtractionError
    from ml.predict_speaker import SpeakerAuthenticator, PredictionError
    from speech.vosk_recognizer import VoskRecognizer, VoskRecognitionError
    from commands.command_interpreter import CommandInterpreter
    from commands.action_executor import ActionExecutor, ActionExecutorError
    from response.tts_engine import ResponseEngine
    from database.db_operations import CommandLogger
    from utils.config import AUDIO_DURATION, AUTHENTICATION_THRESHOLD
    from utils.resource_monitor import ResourceMonitor
except ImportError as e:
    print(f"Warning: Some modules not available in auth_ui: {e}")


class AuthenticationWindow:
    """
    Authentication and command execution window.

    Workflow:
    1. Record voice for authentication
    2. Authenticate speaker
    3. If authenticated, listen for command
    4. Execute command
    5. Provide voice feedback
    """

    def __init__(self, window):
        """
        Initialize authentication window.

        Args:
            window: Tkinter window.
        """
        self.window = window
        self.window.title("Authentication & Command Execution")
        self.window.geometry("750x750")

        # Initialize components
        try:
            print("[INFO] Initializing authentication components...")
            self.authenticator = SpeakerAuthenticator()
            self.command_interpreter = CommandInterpreter()
            self.action_executor = ActionExecutor()
            self.response_engine = ResponseEngine()
            print("[INFO] Core components initialized")
            
            # Initialize recognizer in background (VOSK takes time to load)
            self.recognizer = None
            self.recognizer_loading = True
            print("[INFO] Starting speech recognizer in background thread...")
            
            self.command_logger = CommandLogger()
            print("[INFO] All core components initialized successfully")
        except Exception as e:
            print(f"[ERROR] Initialization failed: {str(e)}")
            messagebox.showerror("Error", f"Failed to initialize: {str(e)}")
            return

        # State variables
        self.authenticated_user = None
        self.is_processing = False
        self.current_audio = None

        # Setup UI
        self._create_widgets()
        
        # Load recognizer in background after UI is created
        thread = threading.Thread(target=self._load_recognizer_background, daemon=True)
        thread.start()

    def _load_recognizer_background(self):
        """Load speech recognizer in background thread (VOSK takes time)."""
        error_message = None
        try:
            print("[INFO] Checking system resources before loading VOSK...")
            
            # Check if it's safe to load VOSK
            is_safe, warning = ResourceMonitor.check_vosk_safety()
            
            if not is_safe:
                print(f"[ERROR] Not safe to load VOSK: {warning}")
                error_message = warning
                self.recognizer_loading = False
                self.window.after(0, lambda: messagebox.showerror(
                    "Insufficient Memory",
                    warning
                ))
                self.window.after(0, lambda: self._update_command_button_status())
                return
            
            if warning:
                print(f"[WARNING] {warning}")
                self.window.after(0, lambda: self.cmd_status_var.set("⚠️ Memory usage high, loading..."))
            
            # Show resource status
            print("[INFO] Current system resources:")
            status = ResourceMonitor.check_resources(verbose=True)
            
            print("[INFO] Loading VOSK model in background (this may take 20-30 seconds)...")
            self.window.after(0, lambda: self.cmd_status_var.set("⏳ Loading VOSK model... (please wait)"))
            
            self.recognizer = self._init_recognizer()
            self.recognizer_loading = False
            
            if self.recognizer:
                print("[SUCCESS] VOSK recognizer loaded and ready!")
                # Check resources after loading
                print("[INFO] Resources after VOSK loaded:")
                status_after = ResourceMonitor.check_resources(verbose=True)
                self.window.after(0, lambda: self._update_command_button_status())
                if self.authenticated_user:
                    self.window.after(0, lambda: self.cmd_status_var.set("✓ Speech recognizer ready!"))
            else:
                print("[WARNING] VOSK recognizer failed to load")
                error_message = "Failed to initialize VOSK recognizer. Check console for details."
                self.window.after(0, lambda: self._update_command_button_status())
                
        except Exception as e:
            print(f"[ERROR] Background recognizer loading failed: {e}")
            import traceback
            traceback.print_exc()
            error_message = f"VOSK Loading Error: {str(e)}"
            self.recognizer_loading = False
            self.window.after(0, lambda: self._update_command_button_status())
        
        # Show error to user if loading failed
        if error_message:
            self.window.after(0, lambda: messagebox.showerror(
                "Speech Recognizer Error",
                f"Could not initialize speech recognizer:\n\n{error_message}\n\n"
                "Solutions:\n"
                "1. Check console output for detailed error\n"
                "2. Verify VOSK installed: pip install vosk\n"
                "3. Verify model in vosk_model/ directory\n"
                "4. Check config.py VOSK_MODEL_DIR path\n\n"
                "Restart the application after fixing."
            ))

    def _update_command_button_status(self):
        """Update command button status after recognizer loads."""
        if self.authenticated_user and self.recognizer:
            self.cmd_btn.config(state=tk.NORMAL)
            self.cmd_status_var.set("✓ Ready to execute command")
        elif self.authenticated_user and not self.recognizer:
            self.cmd_btn.config(state=tk.DISABLED)
            self.cmd_status_var.set("⚠️ Speech recognizer not ready")

    def _init_recognizer(self):
        """Initialize speech recognizer safely."""
        try:
            print("[INFO] Starting speech recognizer initialization...")
            recognizer = VoskRecognizer()
            print("✓ Speech recognizer initialized successfully")
            return recognizer
        except VoskRecognitionError as e:
            print(f"[ERROR] VoskRecognitionError: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
        except ImportError as e:
            print(f"[ERROR] ImportError: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
        except Exception as e:
            print(f"[ERROR] Unexpected error: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def _create_widgets(self):
        """Create authentication window widgets."""

        # Header
        header = ttk.Label(
            self.window,
            text="🔐 Authentication & Command Execution",
            font=("Segoe UI", 16, "bold"),
        )
        header.pack(pady=15)

        # Step 1: Authentication
        auth_frame = ttk.LabelFrame(self.window, text="Step 1: Authentication", padding=15)
        auth_frame.pack(fill=tk.X, padx=20, pady=10)

        self.auth_status_var = tk.StringVar(value="Ready to authenticate")
        self.auth_status = ttk.Label(
            auth_frame,
            textvariable=self.auth_status_var,
            font=("Segoe UI", 10),
            foreground="blue",
        )
        self.auth_status.pack(pady=10)

        ttk.Label(auth_frame, text=f"Duration: {AUDIO_DURATION}s").pack()

        self.auth_btn = ttk.Button(
            auth_frame,
            text="🎤 Record Voice for Authentication",
            command=self._on_authenticate,
        )
        self.auth_btn.pack(pady=10, fill=tk.X)

        # Result frame
        result_frame = ttk.LabelFrame(self.window, text="Authentication Result", padding=15)
        result_frame.pack(fill=tk.X, padx=20, pady=10)

        self.result_var = tk.StringVar(value="Awaiting authentication...")
        self.result_label = ttk.Label(
            result_frame,
            textvariable=self.result_var,
            font=("Segoe UI", 11, "bold"),
            foreground="red",
        )
        self.result_label.pack(pady=10)

        self.confidence_var = tk.StringVar(value="")
        self.confidence_label = ttk.Label(
            result_frame,
            textvariable=self.confidence_var,
            font=("Segoe UI", 10),
        )
        self.confidence_label.pack()

        # Step 2: Command execution
        cmd_frame = ttk.LabelFrame(
            self.window,
            text="Step 2: Command Execution (after authentication)",
            padding=15,
        )
        cmd_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        ttk.Label(cmd_frame, text="Available Commands:").pack(anchor=tk.W)

        # Commands list
        cmd_list = tk.Text(cmd_frame, height=5, width=70, font=("Courier", 9))
        cmd_list.pack(fill=tk.X, pady=10)

        commands_text = "\n".join(self.command_interpreter.list_commands())
        cmd_list.insert(tk.END, commands_text)
        cmd_list.config(state=tk.DISABLED)

        self.cmd_status_var = tk.StringVar(value="Initializing speech recognizer (20-30 seconds)...")
        self.cmd_status = ttk.Label(
            cmd_frame,
            textvariable=self.cmd_status_var,
            font=("Segoe UI", 10),
            foreground="blue",
        )
        self.cmd_status.pack(pady=10)

        self.cmd_btn = ttk.Button(
            cmd_frame,
            text="🎤 Record Voice Command",
            command=self._on_execute_command,
            state=tk.DISABLED,
        )
        self.cmd_btn.pack(pady=10, fill=tk.X)

        # Command result display
        ttk.Label(cmd_frame, text="Command Result:", font=("Segoe UI", 9, "bold")).pack(anchor=tk.W, pady=(10, 5))
        
        self.cmd_result_text = tk.Text(cmd_frame, height=4, width=70, font=("Courier", 9), wrap=tk.WORD)
        self.cmd_result_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.cmd_result_text.config(state=tk.DISABLED)

        # Buttons
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Button(
            button_frame,
            text="❌ Close",
            command=self.window.destroy,
        ).pack(side=tk.RIGHT, padx=5)

    def _on_authenticate(self):
        """Handle authentication."""
        if self.is_processing:
            messagebox.showwarning("Warning", "Already processing")
            return

        self.is_processing = True
        self.auth_btn.config(state=tk.DISABLED)
        self.auth_status_var.set(f"🎤 Recording voice... ({AUDIO_DURATION}s)")
        self.window.update()

        # Run in background
        thread = threading.Thread(target=self._authenticate_thread)
        thread.start()

    def _authenticate_thread(self):
        """Authenticate in background thread."""
        try:
            # Record voice
            recorder = AudioRecorder(duration=AUDIO_DURATION)
            audio = recorder.record(show_progress=False)

            if audio is None:
                self.window.after(0, lambda: self.auth_status_var.set("Authentication cancelled"))
                self.is_processing = False
                self.window.after(0, lambda: self.auth_btn.config(state=tk.NORMAL))
                return

            self.current_audio = audio

            # Extract features
            self.window.after(0, lambda: self.auth_status_var.set("🔄 Extracting features..."))

            extractor = MFCCExtractor()
            features = extractor.get_feature_vector(audio, compute_stats=True)

            # Authenticate
            def safe_set_status():
                try:
                    if self.window.winfo_exists():
                        self.auth_status_var.set("🔐 Authenticating...")
                except:
                    pass
            self.window.after(0, safe_set_status)

            result = self.authenticator.authenticate(features, return_details=True)

            # Update UI
            if result["authenticated"]:
                self.authenticated_user = result["speaker"]
                def safe_update_success():
                    try:
                        if self.window.winfo_exists():
                            self.result_var.set(f"✓ Authenticated as: {self.authenticated_user}")
                            self.result_label.config(foreground="green")
                            self.confidence_var.set(f"Confidence: {result['confidence']:.2%}")
                            self._update_command_button_status()
                    except:
                        pass
                self.window.after(0, safe_update_success)

                # Speak response
                try:
                    self.response_engine.speak_response(
                        "authentication_success",
                        username=self.authenticated_user
                    )
                except:
                    pass

            else:
                def safe_update_fail():
                    try:
                        if self.window.winfo_exists():
                            self.result_var.set("✗ Authentication Failed - Unknown Speaker")
                            self.result_label.config(foreground="red")
                            self.confidence_var.set(f"Confidence: {result['confidence']:.2%} (threshold: {AUTHENTICATION_THRESHOLD:.0%})")
                    except:
                        pass
                self.window.after(0, safe_update_fail)

                try:
                    self.response_engine.speak_response("authentication_failed")
                except:
                    pass

        except RecorderError as e:
            def safe_show_error_1():
                try:
                    if self.window.winfo_exists():
                        messagebox.showerror("Recording Error", str(e))
                        self.auth_status_var.set("Recording failed")
                except:
                    pass
            self.window.after(0, safe_show_error_1)

        except (MFCCExtractionError, PredictionError) as e:
            def safe_show_error_2():
                try:
                    if self.window.winfo_exists():
                        messagebox.showerror("Processing Error", str(e))
                        self.auth_status_var.set("Processing failed")
                except:
                    pass
            self.window.after(0, safe_show_error_2)

        finally:
            self.is_processing = False
            # Safely update button - handle case where window is closed
            def safe_enable_button():
                try:
                    if self.window.winfo_exists():
                        self.auth_btn.config(state=tk.NORMAL)
                except:
                    pass  # Window or widget no longer exists
            
            self.window.after(0, safe_enable_button)

    def _on_execute_command(self):
        """Handle command execution."""
        if not self.authenticated_user:
            messagebox.showerror("Error", "Not authenticated")
            return

        if hasattr(self, 'recognizer_loading') and self.recognizer_loading:
            messagebox.showwarning(
                "Still Loading",
                "Speech recognizer is still loading.\n\n"
                "Please wait 20-30 seconds for it to initialize.\n"
                "Try again in a moment."
            )
            return

        if not self.recognizer:
            messagebox.showerror(
                "Speech Recognizer Not Available",
                "Speech recognizer failed to initialize.\n\n"
                "Please check the console output for error details.\n\n"
                "Common solutions:\n"
                "1. Verify VOSK is installed: pip install vosk\n"
                "2. Check vosk_model/ directory exists and has the model files\n"
                "3. Verify model path in utils/config.py:\n"
                "   VOSK_MODEL_DIR = PROJECT_ROOT / 'vosk_model' / 'vosk-model-en-us-0.42-gigaspeech'\n\n"
                "Restart the application after fixing these issues."
            )
            return

        if self.is_processing:
            messagebox.showwarning("Warning", "Already processing")
            return

        self.is_processing = True
        self.cmd_btn.config(state=tk.DISABLED)
        self.cmd_status_var.set(f"🎤 Recording command... ({AUDIO_DURATION}s)")
        self.window.update()

        # Run in background
        thread = threading.Thread(target=self._command_thread)
        thread.start()

    def _command_thread(self):
        """Execute command in background thread."""
        try:
            # Record command
            self.window.after(0, lambda: self._update_command_result("🎤 Recording your command..."))
            
            recorder = AudioRecorder(duration=AUDIO_DURATION)
            audio = recorder.record(show_progress=False)

            if audio is None:
                self.window.after(0, lambda: self.cmd_status_var.set("Command cancelled"))
                self.window.after(0, lambda: self._update_command_result("⚠️ Recording cancelled"))
                self.is_processing = False
                self.window.after(0, lambda: self.cmd_btn.config(state=tk.NORMAL))
                return

            # Recognize speech
            self.window.after(0, lambda: self.cmd_status_var.set("🔄 Recognizing speech... (this may take a moment)"))
            self.window.after(0, lambda: self._update_command_result("Processing audio..."))

            try:
                print(f"\n[INFO] Audio recorded - shape: {audio.shape}, dtype: {audio.dtype}")
                print(f"[INFO] Audio level - min: {audio.min():.4f}, max: {audio.max():.4f}")
                
                recognized_text = self.recognizer.recognize_audio(audio)
                print(f"[SUCCESS] Recognized text: '{recognized_text}'")
                
                # If still empty after recognition
                if not recognized_text or recognized_text.strip() == "":
                    print("[WARNING] Speech recognition returned empty result")
                    self.window.after(0, lambda: self._update_command_result(
                        "⚠️ No speech recognized\n\n"
                        "Tips:\n"
                        "• Speak clearly\n"
                        "• Speak louder\n"
                        "• Check microphone settings\n"
                        "• Try a common command like 'openapp' or 'plamusic'"
                    ))
                    self.window.after(0, lambda: self.cmd_status_var.set("Ready to execute command"))
                    self.is_processing = False
                    self.window.after(0, lambda: self.cmd_btn.config(state=tk.NORMAL))
                    return
                    
            except VoskRecognitionError as e:
                print(f"[ERROR] Recognition error: {e}")
                self.window.after(0, lambda: messagebox.showwarning("Warning", f"Speech recognition failed: {str(e)}"))
                self.window.after(0, lambda: self.cmd_status_var.set("Speech recognition failed"))
                self.window.after(0, lambda: self._update_command_result(f"❌ Recognition Error\n\n{str(e)}"))
                self.is_processing = False
                self.window.after(0, lambda: self.cmd_btn.config(state=tk.NORMAL))
                return

            self.window.after(0, lambda: self.cmd_status_var.set(f'✓ Recognized: "{recognized_text}"'))

            # Interpret command
            cmd_result = self.command_interpreter.interpret_command(recognized_text)

            if not cmd_result["success"]:
                self.window.after(0, lambda: self._update_command_result(
                    f"❌ COMMAND NOT RECOGNIZED\n\n"
                    f"You said: '{recognized_text}'\n\n"
                    f"Available commands:\n"
                    f"• openapp\n"
                    f"• closefile\n"
                    f"• createdir\n"
                    f"• deletedir\n"
                    f"• playmusic\n"
                    f"• checkstatus\n\n"
                    f"Try speaking one of these commands."
                ))
                try:
                    self.response_engine.speak_response("command_unknown")
                except:
                    pass
            else:
                # Execute command
                self.window.after(0, lambda: self.cmd_status_var.set(f"⚙️ Executing: {cmd_result['command']}"))

                try:
                    exec_result = self.action_executor.execute_from_command_result(
                        cmd_result,
                        username=self.authenticated_user
                    )

                    if exec_result.get("success"):
                        result_text = f"✓ COMMAND EXECUTED\n" \
                                    f"Command: {cmd_result['command']}\n" \
                                    f"User: {self.authenticated_user}\n" \
                                    f"Status: {exec_result.get('message', 'Success')}"
                        self.window.after(0, lambda: self._update_command_result(result_text))
                        try:
                            self.response_engine.speak_response("command_executed")
                        except:
                            pass
                    else:
                        result_text = f"❌ EXECUTION FAILED\n" \
                                    f"Command: {cmd_result['command']}\n" \
                                    f"Error: {exec_result.get('message', 'Unknown error')}"
                        self.window.after(0, lambda: self._update_command_result(result_text))
                        try:
                            self.response_engine.speak_response("command_failed")
                        except:
                            pass

                except ActionExecutorError as e:
                    self.window.after(0, lambda: self._update_command_result(f"❌ EXECUTOR ERROR\n{str(e)}"))

            self.window.after(0, lambda: self.cmd_status_var.set("Ready to execute command"))

        except RecorderError as e:
            self.window.after(0, lambda: messagebox.showerror("Recording Error", str(e)))
            self.window.after(0, lambda: self.cmd_status_var.set("Recording failed"))

        finally:
            self.is_processing = False
            self.window.after(0, lambda: self.cmd_btn.config(state=tk.NORMAL))

    def _update_command_result(self, result_text):
        """Update command result text widget with new result."""
        self.cmd_result_text.config(state=tk.NORMAL)
        self.cmd_result_text.delete(1.0, tk.END)
        self.cmd_result_text.insert(tk.END, result_text)
        self.cmd_result_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    AuthenticationWindow(root)
    root.mainloop()
