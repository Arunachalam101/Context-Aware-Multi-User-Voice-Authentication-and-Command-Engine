"""
Command interpreter module for voice command processing.

Maps recognized speech text to predefined commands and extracts
command parameters.
"""

import re
from difflib import SequenceMatcher
from pathlib import Path

# Import configuration
try:
    from utils.config import COMMANDS
except ImportError:
    COMMANDS = {
        "open notepad": "notepad",
        "open calculator": "calc",
        "open cmd": "cmd",
        "tell time": "time",
        "system info": "systeminfo",
        "open file explorer": "explorer",
    }


class CommandInterpreterError(Exception):
    """Raised when command interpretation fails."""

    pass


class CommandInterpreter:
    """
    Interprets voice commands and maps them to actions.

    Provides methods to:
    - Match voice text to predefined commands
    - Handle fuzzy matching for error tolerance
    - Extract command parameters
    - Get command suggestions
    """

    def __init__(self, commands=None, fuzzy_threshold=0.7):
        """
        Initialize command interpreter.

        Args:
            commands (dict, optional): Dictionary mapping commands to actions.
            fuzzy_threshold (float): Similarity threshold for fuzzy matching (0-1).
        """
        self.commands = commands or COMMANDS
        self.fuzzy_threshold = fuzzy_threshold
        # Precompile command patterns for faster matching
        self.command_keys = list(self.commands.keys())

    def normalize_text(self, text):
        """
        Normalize voice text for matching.

        Args:
            text (str): Raw voice text.

        Returns:
            str: Normalized text.
        """
        # Convert to lowercase
        text = text.lower().strip()
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def exact_match(self, text):
        """
        Try exact command match.

        Args:
            text (str): Voice text.

        Returns:
            tuple: (command, action) or (None, None) if no match.
        """
        normalized = self.normalize_text(text)

        for command in self.command_keys:
            if self.normalize_text(command) == normalized:
                return command, self.commands[command]

        return None, None

    def fuzzy_match(self, text):
        """
        Try fuzzy command matching using sequence similarity.

        Args:
            text (str): Voice text.

        Returns:
            tuple: (command, action, similarity) or (None, None, 0).
        """
        normalized = self.normalize_text(text)
        best_match = None
        best_similarity = 0

        for command in self.command_keys:
            similarity = SequenceMatcher(
                None,
                normalized,
                self.normalize_text(command)
            ).ratio()

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = command

        if best_similarity >= self.fuzzy_threshold:
            return best_match, self.commands[best_match], best_similarity

        return None, None, 0

    def interpret_command(self, text, use_fuzzy=True):
        """
        Interpret voice text and map to command.

        Args:
            text (str): Voice text.
            use_fuzzy (bool): Use fuzzy matching if exact match fails.

        Returns:
            dict: Command interpretation result.
        """
        try:
            # Try exact match first
            command, action = self.exact_match(text)

            if command:
                return {
                    "success": True,
                    "command": command,
                    "action": action,
                    "match_type": "exact",
                    "confidence": 1.0,
                    "text": text,
                }

            # Try fuzzy match if enabled
            if use_fuzzy:
                command, action, similarity = self.fuzzy_match(text)

                if command:
                    return {
                        "success": True,
                        "command": command,
                        "action": action,
                        "match_type": "fuzzy",
                        "confidence": similarity,
                        "text": text,
                    }

            # No match found
            return {
                "success": False,
                "command": None,
                "action": None,
                "match_type": None,
                "confidence": 0.0,
                "text": text,
                "error": f"No matching command for '{text}'",
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    def get_suggestions(self, text, num_suggestions=3):
        """
        Get command suggestions for partial/unclear text.

        Args:
            text (str): Voice text.
            num_suggestions (int): Number of suggestions to return.

        Returns:
            list: List of (command, similarity) tuples, sorted by similarity.
        """
        normalized = self.normalize_text(text)
        similarities = []

        for command in self.command_keys:
            similarity = SequenceMatcher(
                None,
                normalized,
                self.normalize_text(command)
            ).ratio()
            similarities.append((command, similarity))

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top suggestions
        return similarities[:num_suggestions]

    def list_commands(self):
        """
        Get list of all available commands.

        Returns:
            list: List of command strings.
        """
        return self.command_keys.copy()

    def add_command(self, command_text, action):
        """
        Add a new command dynamically.

        Args:
            command_text (str): Command text.
            action (str): Action to execute.
        """
        command_text = command_text.lower().strip()
        if command_text not in self.commands:
            self.commands[command_text] = action
            self.command_keys = list(self.commands.keys())
            print(f"✓ Command added: '{command_text}' -> '{action}'")
        else:
            print(f"⚠ Command already exists: '{command_text}'")

    def remove_command(self, command_text):
        """
        Remove a command.

        Args:
            command_text (str): Command text to remove.

        Returns:
            bool: True if removed, False if not found.
        """
        command_text = command_text.lower().strip()
        if command_text in self.commands:
            del self.commands[command_text]
            self.command_keys = list(self.commands.keys())
            print(f"✓ Command removed: '{command_text}'")
            return True
        return False


def interpret_voice_command(text, commands=None):
    """
    Convenience function for one-shot command interpretation.

    Args:
        text (str): Voice text.
        commands (dict, optional): Command dictionary.

    Returns:
        dict: Interpretation result.
    """
    interpreter = CommandInterpreter(commands)
    return interpreter.interpret_command(text)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Command Interpreter - Test Mode")
    print("=" * 70 + "\n")

    try:
        # Initialize interpreter
        interpreter = CommandInterpreter()

        print("Available commands:")
        for cmd in interpreter.list_commands():
            print(f"  - {cmd}")

        print("\n" + "-" * 70)
        print("Testing command interpretation:\n")

        # Test cases
        test_cases = [
            "open notepad",
            "open calculator",
            "tell time",
            "open notepd",  # Typo
            "open calc",  # Abbreviation
            "unknown command",
        ]

        for text in test_cases:
            result = interpreter.interpret_command(text)
            print(f"Input: '{text}'")
            print(f"  Success: {result['success']}")
            if result['success']:
                print(f"  Command: '{result['command']}'")
                print(f"  Action: '{result['action']}'")
                print(f"  Match type: {result['match_type']}")
                print(f"  Confidence: {result['confidence']:.2%}")
            else:
                print(f"  Error: {result.get('error', 'Unknown error')}")
                # Show suggestions
                suggestions = interpreter.get_suggestions(text)
                if suggestions:
                    print(f"  Suggestions:")
                    for cmd, sim in suggestions:
                        print(f"    - {cmd} ({sim:.2%})")
            print()

        print("✓ Command interpreter test completed!")

    except Exception as e:
        print(f"✗ Test failed: {str(e)}")
