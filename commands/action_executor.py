"""
Action executor module for voice authentication system.

Executes system commands and actions based on voice commands.
Handles system-level operations safely and with logging.
"""

import subprocess
import datetime
from pathlib import Path
import sys
import platform

# Import configuration
try:
    from utils.config import COMMANDS
    from database.db_operations import CommandLogger
except ImportError:
    COMMANDS = {}
    CommandLogger = None


class ActionExecutorError(Exception):
    """Raised when action execution fails."""

    pass


class ActionExecutor:
    """
    Executes system actions based on mapped commands.

    Provides methods to:
    - Execute system commands
    - Get time and system information
    - Handle errors safely
    - Log executed commands
    - Support both built-in and custom actions
    """

    def __init__(self, command_logger=None):
        """
        Initialize action executor.

        Args:
            command_logger (CommandLogger, optional): Logger for command execution.
        """
        self.command_logger = command_logger
        self.last_execution = None
        self.is_windows = platform.system() == "Windows"
        self.shell = True if self.is_windows else False

    def execute_system_command(self, command):
        """
        Execute a system command.

        Args:
            command (str): System command to execute.

        Returns:
            dict: Execution result with output and status.

        Raises:
            ActionExecutorError: If execution fails.
        """
        try:
            print(f"📤 Executing: {command}")

            result = subprocess.run(
                command,
                shell=self.shell,
                capture_output=True,
                text=True,
                timeout=10,
            )

            output = result.stdout.strip() if result.stdout else ""

            return {
                "success": result.returncode == 0,
                "command": command,
                "output": output,
                "error": result.stderr if result.returncode != 0 else None,
                "return_code": result.returncode,
            }

        except subprocess.TimeoutExpired:
            raise ActionExecutorError(f"Command timeout: {command}")
        except Exception as e:
            raise ActionExecutorError(f"Failed to execute command: {str(e)}")

    def get_system_time(self):
        """
        Get current system time (built-in action).

        Returns:
            str: Current time as formatted string.
        """
        now = datetime.datetime.now()
        return now.strftime("%I:%M %p")

    def get_system_info(self):
        """
        Get system information (built-in action).

        Returns:
            dict: System information.
        """
        return {
            "system": platform.system(),
            "platform": platform.platform(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        }

    def tell_time(self):
        """
        Built-in action: Tell current time.

        Returns:
            dict: Response with time information.
        """
        current_time = self.get_system_time()
        return {
            "success": True,
            "action": "tell_time",
            "time": current_time,
            "response": f"The current time is {current_time}",
        }

    def open_application(self, application):
        """
        Built-in action: Open system application.

        Args:
            application (str): Application name or command.

        Returns:
            dict: Execution result.
        """
        try:
            # Map friendly names to commands
            app_map = {
                "notepad": "notepad" if self.is_windows else "gedit",
                "calculator": "calc" if self.is_windows else "gnome-calculator",
                "calculator": "calc" if self.is_windows else "bc",
                "cmd": "cmd" if self.is_windows else "bash",
                "explorer": "explorer" if self.is_windows else "nautilus",
                "file explorer": "explorer" if self.is_windows else "nautilus",
            }

            actual_cmd = app_map.get(application.lower(), application)
            result = self.execute_system_command(actual_cmd)

            return {
                "success": result["success"],
                "action": "open_application",
                "application": application,
                "response": f"Opening {application}",
                "execution_details": result,
            }

        except Exception as e:
            raise ActionExecutorError(f"Failed to open application: {str(e)}")

    def execute_action(self, action_name, parameters=None):
        """
        Execute an action by name.

        Args:
            action_name (str): Name/command of action to execute.
            parameters (dict, optional): Parameters for the action.

        Returns:
            dict: Execution result.

        Raises:
            ActionExecutorError: If execution fails.
        """
        try:
            parameters = parameters or {}

            # Handle built-in actions
            if action_name == "time":
                return self.tell_time()

            elif action_name == "system info":
                info = self.get_system_info()
                return {
                    "success": True,
                    "action": "system_info",
                    "system_info": info,
                    "response": f"System: {info['system']} {info['platform']}",
                }

            elif action_name == "notepad":
                return self.open_application("notepad")

            elif action_name == "calc":
                return self.open_application("calculator")

            elif action_name == "cmd":
                return self.open_application("cmd")

            elif action_name == "explorer":
                return self.open_application("file explorer")

            else:
                # Try to execute as system command
                result = self.execute_system_command(action_name)
                return {
                    "success": result["success"],
                    "action": action_name,
                    "execution_details": result,
                }

        except Exception as e:
            raise ActionExecutorError(f"Action execution failed: {str(e)}")

    def execute_from_command_result(self, command_result, username=None):
        """
        Execute action from command interpreter result.

        Args:
            command_result (dict): Result from command interpreter.
            username (str, optional): Username executing the command.

        Returns:
            dict: Execution result with logging.

        Raises:
            ActionExecutorError: If execution fails.
        """
        try:
            if not command_result.get("success"):
                return {
                    "success": False,
                    "error": command_result.get("error", "Command not recognized"),
                }

            action = command_result.get("action")
            result = self.execute_action(action)

            # Log command execution
            if self.command_logger and username:
                try:
                    self.command_logger.log_command(
                        username,
                        command_result.get("command", action),
                        "executed" if result.get("success") else "failed",
                    )
                except:
                    pass  # Don't fail execution if logging fails

            self.last_execution = result
            return result

        except ActionExecutorError as e:
            raise ActionExecutorError(f"Execution failed: {str(e)}")

    def get_last_execution(self):
        """
        Get information about last executed action.

        Returns:
            dict: Last execution result or None.
        """
        return self.last_execution


def execute_voice_command(action_name, username=None):
    """
    Convenience function for one-shot command execution.

    Args:
        action_name (str): Action name or command.
        username (str, optional): Username executing the command.

    Returns:
        dict: Execution result.

    Raises:
        ActionExecutorError: If execution fails.
    """
    executor = ActionExecutor()
    return executor.execute_action(action_name)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Action Executor - Test Mode")
    print("=" * 70 + "\n")

    try:
        # Initialize executor
        executor = ActionExecutor()

        print("Testing built-in actions:\n")

        # Test time action
        print("1. Tell Time:")
        result = executor.tell_time()
        print(f"   Response: {result['response']}\n")

        # Test system info action
        print("2. System Info:")
        result = executor.execute_action("system info")
        print(f"   Response: {result['response']}\n")

        # Test application opening (don't actually open)
        print("3. Open Notepad (would open in real execution):")
        print(f"   Command: notepad\n")

        print("✓ Action executor test completed!")

    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
