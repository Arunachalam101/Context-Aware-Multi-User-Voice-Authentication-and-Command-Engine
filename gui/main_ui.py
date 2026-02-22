"""
Main GUI interface for Voice Authentication System.

Provides main control panel with buttons for:
- User registration
- Model training
- Authentication and command mode
- Exit
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import threading

# Import all modules
try:
    from gui.register_ui import RegisterWindow
    from gui.auth_ui import AuthenticationWindow
    from ml.train_model import train_model_from_database, ModelTrainingError
    from database.db_operations import UserManager, VoiceFeatureManager
    from utils.config import APP_NAME, APP_VERSION, create_directories
except ImportError:
    # Fallback imports
    RegisterWindow = None
    AuthenticationWindow = None


class MainWindow:
    """
    Main application window for voice authentication system.

    Provides buttons for:
    - Register new user
    - Train speaker recognition model
    - Authenticate and execute commands
    - View registered users
    - Exit application
    """

    def __init__(self, root):
        """
        Initialize main window.

        Args:
            root: Tkinter root window.
        """
        self.root = root
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # Initialize database managers
        try:
            self.user_manager = UserManager()
            self.feature_manager = VoiceFeatureManager()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize database: {str(e)}")
            return

        # Setup UI
        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        """Configure ttk styles for modern appearance."""
        style = ttk.Style()
        style.theme_use("clam")

        # Configure button style
        style.configure(
            "Large.TButton",
            font=("Segoe UI", 12, "bold"),
            padding=20,
        )

        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 18, "bold"),
            background="lightblue",
        )

        style.configure(
            "Info.TLabel",
            font=("Segoe UI", 10),
        )

    def _create_widgets(self):
        """Create main window widgets."""

        # Header frame
        header_frame = ttk.Frame(self.root, height=80)
        header_frame.pack(fill=tk.X, padx=20, pady=10)

        header_label = ttk.Label(
            header_frame,
            text=f"🎤 {APP_NAME}",
            font=("Segoe UI", 20, "bold"),
        )
        header_label.pack(pady=10)

        subtitle = ttk.Label(
            header_frame,
            text="Offline Voice Authentication and Command Execution",
            font=("Segoe UI", 11),
        )
        subtitle.pack()

        # Separator
        ttk.Separator(self.root, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10)

        # Main button frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Register button
        self.register_btn = ttk.Button(
            button_frame,
            text="📝 Register New User",
            command=self._on_register,
            style="Large.TButton",
        )
        self.register_btn.pack(fill=tk.X, pady=10)

        # Train model button
        self.train_btn = ttk.Button(
            button_frame,
            text="🧠 Train Speaker Model",
            command=self._on_train,
            style="Large.TButton",
        )
        self.train_btn.pack(fill=tk.X, pady=10)

        # Authenticate button
        self.auth_btn = ttk.Button(
            button_frame,
            text="🔐 Authenticate & Command",
            command=self._on_authenticate,
            style="Large.TButton",
        )
        self.auth_btn.pack(fill=tk.X, pady=10)

        # View users button
        self.users_btn = ttk.Button(
            button_frame,
            text="👥 View Registered Users",
            command=self._on_view_users,
            style="Large.TButton",
        )
        self.users_btn.pack(fill=tk.X, pady=10)

        # Delete user button
        self.delete_btn = ttk.Button(
            button_frame,
            text="🗑️ Delete User",
            command=self._on_delete_user,
            style="Large.TButton",
        )
        self.delete_btn.pack(fill=tk.X, pady=10)

        # Exit button
        self.exit_btn = ttk.Button(
            button_frame,
            text="❌ Exit",
            command=self._on_exit,
            style="Large.TButton",
        )
        self.exit_btn.pack(fill=tk.X, pady=10)

        # Status frame
        status_frame = ttk.LabelFrame(self.root, text="Status", padding=10)
        status_frame.pack(fill=tk.X, padx=20, pady=10)

        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
        )
        self.status_label.pack()

        # Info frame
        info_frame = ttk.LabelFrame(self.root, text="System Info", padding=10)
        info_frame.pack(fill=tk.X, padx=20, pady=5)

        self._update_info()
        self.info_label = ttk.Label(info_frame, text="", font=("Segoe UI", 9))
        self.info_label.pack(anchor=tk.W)

    def _update_info(self):
        """Update system information."""
        try:
            users = self.user_manager.list_all_users()
            info_text = f"Registered Users: {len(users)}"
            self.info_label.config(text=info_text)
        except:
            pass

    def _on_register(self):
        """Handle register button click."""
        try:
            if RegisterWindow is None:
                messagebox.showerror("Error", "Registration module not available")
                return

            register_win = tk.Toplevel(self.root)
            RegisterWindow(register_win)
            self.status_var.set("User registration window opened")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open registration: {str(e)}")

    def _on_train(self):
        """Handle train model button click."""
        try:
            self.train_btn.config(state=tk.DISABLED)
            self.status_var.set("Training model... (this may take a moment)")
            self.root.update()

            # Run training in separate thread to prevent UI freeze
            thread = threading.Thread(target=self._train_model_thread)
            thread.start()

        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {str(e)}")
            self.train_btn.config(state=tk.NORMAL)

    def _train_model_thread(self):
        """Train model in background thread."""
        try:
            train_model_from_database()
            self.root.after(0, lambda: self.status_var.set("✓ Model training completed successfully!"))
            self.root.after(0, lambda: messagebox.showinfo("Success", "Model trained and saved successfully!"))

        except ModelTrainingError as e:
            self.root.after(0, lambda: messagebox.showerror("Training Error", f"Failed to train model:\n\n{str(e)}"))
            self.root.after(0, lambda: self.status_var.set("Model training failed"))

        finally:
            self.root.after(0, lambda: self.train_btn.config(state=tk.NORMAL))

    def _on_authenticate(self):
        """Handle authenticate button click."""
        try:
            if AuthenticationWindow is None:
                messagebox.showerror("Error", "Authentication module not available")
                return

            auth_win = tk.Toplevel(self.root)
            AuthenticationWindow(auth_win)
            self.status_var.set("Authentication window opened")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open authentication: {str(e)}")

    def _on_view_users(self):
        """Show registered users."""
        try:
            users = self.user_manager.list_all_users()

            if not users:
                messagebox.showinfo("Users", "No registered users found")
                return

            # Create user list window
            user_window = tk.Toplevel(self.root)
            user_window.title("Registered Users")
            user_window.geometry("400x300")

            # Create text widget
            text_widget = tk.Text(user_window, height=15, width=50)
            text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            # Add users
            text_widget.insert(tk.END, "Registered Users:\n\n")
            for i, user in enumerate(users, 1):
                features_count = self.feature_manager.get_feature_count_for_user(user["name"])
                text_widget.insert(
                    tk.END,
                    f"{i}. {user['name']} (ID: {user['id']}, "
                    f"Samples: {features_count})\n"
                )

            text_widget.config(state=tk.DISABLED)

            self.status_var.set(f"Showing {len(users)} registered users")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to list users: {str(e)}")

    def _on_delete_user(self):
        """Handle delete user button click."""
        try:
            users = self.user_manager.list_all_users()

            if not users:
                messagebox.showinfo("Delete User", "No registered users found")
                return

            # Create user selection window
            delete_window = tk.Toplevel(self.root)
            delete_window.title("Delete User")
            delete_window.geometry("400x350")
            delete_window.resizable(False, False)

            # Header
            header = ttk.Label(
                delete_window,
                text="⚠️ Delete User",
                font=("Segoe UI", 14, "bold"),
            )
            header.pack(pady=10)

            # Info message
            info = ttk.Label(
                delete_window,
                text="Select a user to delete (this cannot be undone):",
                font=("Segoe UI", 10),
            )
            info.pack(pady=5)

            # Listbox for users
            frame = ttk.Frame(delete_window)
            frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            scrollbar = ttk.Scrollbar(frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            user_listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, height=12)
            user_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.config(command=user_listbox.yview)

            # Add users to listbox
            user_names = []
            for user in users:
                features_count = self.feature_manager.get_feature_count_for_user(user["name"])
                display_text = f"{user['name']} ({features_count} samples)"
                user_listbox.insert(tk.END, display_text)
                user_names.append(user["name"])

            # Buttons frame
            button_frame = ttk.Frame(delete_window)
            button_frame.pack(fill=tk.X, padx=10, pady=10)

            def delete_selected():
                """Delete the selected user."""
                selection = user_listbox.curselection()
                if not selection:
                    messagebox.showwarning("Warning", "Please select a user to delete")
                    return

                selected_index = selection[0]
                selected_user = user_names[selected_index]

                # Ask for confirmation
                if messagebox.askyesno(
                    "Confirm Delete",
                    f"Are you sure you want to delete user '{selected_user}'?\n\n"
                    "This will delete all voice samples and associated data.",
                ):
                    try:
                        # Delete user and all associated data (cascading delete)
                        self.user_manager.delete_user(selected_user)

                        messagebox.showinfo(
                            "Success",
                            f"User '{selected_user}' has been deleted successfully!",
                        )

                        # Update info and close window
                        self._update_info()
                        self.status_var.set(f"User '{selected_user}' deleted")
                        delete_window.destroy()

                    except Exception as e:
                        messagebox.showerror(
                            "Error",
                            f"Failed to delete user: {str(e)}",
                        )

            delete_btn = ttk.Button(
                button_frame,
                text="🗑️ Delete Selected",
                command=delete_selected,
            )
            delete_btn.pack(side=tk.LEFT, padx=5)

            cancel_btn = ttk.Button(
                button_frame,
                text="❌ Cancel",
                command=delete_window.destroy,
            )
            cancel_btn.pack(side=tk.LEFT, padx=5)

            self.status_var.set("User deletion window opened")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to open delete user window: {str(e)}")

    def _on_exit(self):
        """Handle exit button click."""
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.quit()


def launch_main_ui():
    """Launch the main UI window."""
    root = tk.Tk()
    main_window = MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    # Ensure directories exist
    create_directories()

    # Launch main UI
    launch_main_ui()
