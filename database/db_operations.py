"""
Database operations module for Voice Authentication Engine.

Handles all database operations including:
- User registration and management
- Storing and retrieving voice features
- Managing command logs
"""

import numpy as np
import sqlite3
from pathlib import Path
import sys

# Import database connection
try:
    from database.db_connection import DatabaseConnection, DatabaseError
except ImportError:
    from db_connection import DatabaseConnection, DatabaseError

# Import configuration
try:
    from utils.config import DATABASE_FILE
except ImportError:
    DATABASE_FILE = Path("database/voice_auth.db")


class DBOperationsError(Exception):
    """Raised when database operations fail."""

    pass


class UserManager:
    """
    Manages user database operations.

    Provides methods to:
    - Register new users
    - Retrieve user information
    - Delete users
    - List all users
    """

    def __init__(self, db_connection=None):
        """
        Initialize user manager.

        Args:
            db_connection (DatabaseConnection, optional): Database connection.
                If None, uses singleton instance.
        """
        if db_connection is None:
            self.db = DatabaseConnection.get_instance(DATABASE_FILE)
        else:
            self.db = db_connection

    def register_user(self, username, role="user"):
        """
        Register a new user in the database.

        Args:
            username (str): Unique username.
            role (str): User role (default: 'user').

        Returns:
            int: User ID of registered user.

        Raises:
            DBOperationsError: If registration fails.
        """
        try:
            query = "INSERT INTO users (name, role) VALUES (?, ?)"
            user_id = self.db.execute_insert(query, (username, role))
            print(f"[OK] User registered: {username} (ID: {user_id})")
            return user_id

        except DatabaseError as e:
            if "UNIQUE constraint failed" in str(e):
                raise DBOperationsError(f"Username already exists: {username}")
            raise DBOperationsError(f"Failed to register user: {str(e)}")

    def get_user(self, username):
        """
        Retrieve user information by username.

        Args:
            username (str): Username to retrieve.

        Returns:
            dict: User information (id, name, role, created_at) or None if not found.
        """
        try:
            query = "SELECT id, name, role, created_at FROM users WHERE name = ?"
            result = self.db.execute_query(query, (username,))

            if result:
                row = result[0]
                return {
                    "id": row[0],
                    "name": row[1],
                    "role": row[2],
                    "created_at": row[3],
                }
            return None

        except Exception as e:
            raise DBOperationsError(f"Failed to get user: {str(e)}")

    def get_user_by_id(self, user_id):
        """
        Retrieve user information by user ID.

        Args:
            user_id (int): User ID to retrieve.

        Returns:
            dict: User information or None if not found.
        """
        try:
            query = "SELECT id, name, role, created_at FROM users WHERE id = ?"
            result = self.db.execute_query(query, (user_id,))

            if result:
                row = result[0]
                return {
                    "id": row[0],
                    "name": row[1],
                    "role": row[2],
                    "created_at": row[3],
                }
            return None

        except Exception as e:
            raise DBOperationsError(f"Failed to get user by ID: {str(e)}")

    def user_exists(self, username):
        """
        Check if a user exists.

        Args:
            username (str): Username to check.

        Returns:
            bool: True if user exists, False otherwise.
        """
        return self.get_user(username) is not None

    def list_all_users(self):
        """
        Retrieve all users from database.

        Returns:
            list: List of user dictionaries.
        """
        try:
            query = "SELECT id, name, role, created_at FROM users ORDER BY created_at DESC"
            results = self.db.execute_query(query)

            users = []
            for row in results:
                users.append({
                    "id": row[0],
                    "name": row[1],
                    "role": row[2],
                    "created_at": row[3],
                })
            return users

        except Exception as e:
            raise DBOperationsError(f"Failed to list users: {str(e)}")

    def delete_user(self, username):
        """
        Delete a user and all associated data (cascading delete).

        Args:
            username (str): Username to delete.

        Returns:
            int: Number of rows deleted.

        Raises:
            DBOperationsError: If deletion fails.
        """
        try:
            # Get user ID first
            user = self.get_user(username)
            if user is None:
                raise DBOperationsError(f"User not found: {username}")

            # Delete user (cascading delete will remove features and logs)
            query = "DELETE FROM users WHERE id = ?"
            rows = self.db.execute_update(query, (user["id"],))
            print(f"[OK] User deleted: {username}")
            return rows

        except Exception as e:
            raise DBOperationsError(f"Failed to delete user: {str(e)}")


class VoiceFeatureManager:
    """
    Manages voice feature database operations.

    Provides methods to:
    - Store voice features for users
    - Retrieve features for users
    - Get all features for training
    - Delete features
    """

    def __init__(self, db_connection=None):
        """
        Initialize feature manager.

        Args:
            db_connection (DatabaseConnection, optional): Database connection.
        """
        if db_connection is None:
            self.db = DatabaseConnection.get_instance(DATABASE_FILE)
        else:
            self.db = db_connection

        self.user_manager = UserManager(self.db)

    def store_feature(self, username, feature_vector):
        """
        Store a voice feature vector for a user.

        Args:
            username (str): Username for which to store features.
            feature_vector (np.ndarray): MFCC feature vector.

        Returns:
            int: Feature ID.

        Raises:
            DBOperationsError: If storage fails.
        """
        try:
            # Get user ID
            user = self.user_manager.get_user(username)
            if user is None:
                raise DBOperationsError(f"User not found: {username}")

            # Convert numpy array to bytes for storage
            feature_blob = feature_vector.astype(np.float32).tobytes()

            # Store in database
            query = "INSERT INTO voice_features (user_id, feature_vector) VALUES (?, ?)"
            feature_id = self.db.execute_insert(query, (user["id"], feature_blob))

            print(f"[OK] Feature stored for user {username} (Feature ID: {feature_id})")
            return feature_id

        except Exception as e:
            raise DBOperationsError(f"Failed to store feature: {str(e)}")

    def get_features_for_user(self, username):
        """
        Retrieve all voice features for a specific user.

        Args:
            username (str): Username to retrieve features for.

        Returns:
            list: List of numpy arrays (feature vectors).

        Raises:
            DBOperationsError: If retrieval fails.
        """
        try:
            user = self.user_manager.get_user(username)
            if user is None:
                raise DBOperationsError(f"User not found: {username}")

            query = "SELECT feature_vector FROM voice_features WHERE user_id = ? ORDER BY created_at"
            results = self.db.execute_query(query, (user["id"],))

            features = []
            for row in results:
                # Convert bytes back to numpy array
                feature_vector = np.frombuffer(row[0], dtype=np.float32)
                features.append(feature_vector)

            return features

        except Exception as e:
            raise DBOperationsError(f"Failed to get features: {str(e)}")

    def get_feature_count_for_user(self, username):
        """
        Get number of stored features for a user.

        Args:
            username (str): Username.

        Returns:
            int: Number of stored features.
        """
        try:
            user = self.user_manager.get_user(username)
            if user is None:
                return 0

            query = "SELECT COUNT(*) FROM voice_features WHERE user_id = ?"
            result = self.db.execute_query(query, (user["id"],))
            return result[0][0] if result else 0

        except Exception:
            return 0

    def get_all_features(self):
        """
        Retrieve all voice features from all users for training.

        Returns:
            tuple: (feature_vectors, user_ids)
                - feature_vectors: List of numpy arrays
                - user_ids: List corresponding user IDs
        """
        try:
            query = """
                SELECT vf.feature_vector, vf.user_id
                FROM voice_features vf
                ORDER BY vf.user_id, vf.created_at
            """
            results = self.db.execute_query(query)

            feature_vectors = []
            user_ids = []

            for row in results:
                # Convert bytes back to numpy array
                feature_vector = np.frombuffer(row[0], dtype=np.float32)
                feature_vectors.append(feature_vector)
                user_ids.append(row[1])

            return feature_vectors, user_ids

        except Exception as e:
            raise DBOperationsError(f"Failed to get all features: {str(e)}")

    def get_features_with_usernames(self):
        """
        Retrieve all features with corresponding usernames.

        Returns:
            tuple: (feature_vectors, usernames)
        """
        try:
            query = """
                SELECT vf.feature_vector, u.name
                FROM voice_features vf
                JOIN users u ON vf.user_id = u.id
                ORDER BY u.id, vf.created_at
            """
            results = self.db.execute_query(query)

            feature_vectors = []
            usernames = []

            for row in results:
                feature_vector = np.frombuffer(row[0], dtype=np.float32)
                feature_vectors.append(feature_vector)
                usernames.append(row[1])

            return feature_vectors, usernames

        except Exception as e:
            raise DBOperationsError(f"Failed to get features with usernames: {str(e)}")

    def delete_features_for_user(self, username):
        """
        Delete all features for a user.

        Args:
            username (str): Username.

        Returns:
            int: Number of features deleted.
        """
        try:
            user = self.user_manager.get_user(username)
            if user is None:
                raise DBOperationsError(f"User not found: {username}")

            query = "DELETE FROM voice_features WHERE user_id = ?"
            rows = self.db.execute_update(query, (user["id"],))
            print(f"✓ {rows} features deleted for user {username}")
            return rows

        except Exception as e:
            raise DBOperationsError(f"Failed to delete features: {str(e)}")


class CommandLogger:
    """
    Manages command execution logging.

    Provides methods to:
    - Log executed commands
    - Retrieve command history
    - Get user statistics
    """

    def __init__(self, db_connection=None):
        """Initialize command logger."""
        if db_connection is None:
            self.db = DatabaseConnection.get_instance(DATABASE_FILE)
        else:
            self.db = db_connection

        self.user_manager = UserManager(self.db)

    def log_command(self, username, command, status="executed"):
        """
        Log a command execution.

        Args:
            username (str): Username who executed command.
            command (str): Command executed.
            status (str): Execution status (executed, failed, etc.).

        Returns:
            int: Log ID.
        """
        try:
            user = self.user_manager.get_user(username)
            if user is None:
                raise DBOperationsError(f"User not found: {username}")

            query = """
                INSERT INTO command_logs (user_id, command, status)
                VALUES (?, ?, ?)
            """
            log_id = self.db.execute_insert(query, (user["id"], command, status))
            return log_id

        except Exception as e:
            raise DBOperationsError(f"Failed to log command: {str(e)}")

    def get_user_command_history(self, username, limit=50):
        """
        Get command execution history for a user.

        Args:
            username (str): Username.
            limit (int): Maximum number of records to retrieve.

        Returns:
            list: List of command log records.
        """
        try:
            user = self.user_manager.get_user(username)
            if user is None:
                return []

            query = """
                SELECT id, command, status, timestamp
                FROM command_logs
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """
            results = self.db.execute_query(query, (user["id"], limit))

            records = []
            for row in results:
                records.append({
                    "id": row[0],
                    "command": row[1],
                    "status": row[2],
                    "timestamp": row[3],
                })
            return records

        except Exception as e:
            raise DBOperationsError(f"Failed to get command history: {str(e)}")

    def get_all_command_history(self, limit=100):
        """Get all command history across all users."""
        try:
            query = """
                SELECT u.name, c.command, c.status, c.timestamp
                FROM command_logs c
                JOIN users u ON c.user_id = u.id
                ORDER BY c.timestamp DESC
                LIMIT ?
            """
            results = self.db.execute_query(query, (limit,))

            records = []
            for row in results:
                records.append({
                    "username": row[0],
                    "command": row[1],
                    "status": row[2],
                    "timestamp": row[3],
                })
            return records

        except Exception as e:
            raise DBOperationsError(f"Failed to get all history: {str(e)}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Database Operations - Test Mode")
    print("=" * 70 + "\n")

    try:
        # Initialize managers
        user_manager = UserManager()
        feature_manager = VoiceFeatureManager()
        command_logger = CommandLogger()

        # Test user operations
        print("1. Testing User Registration...")
        user_id = user_manager.register_user("john_doe", "user")
        print(f"   Registered user with ID: {user_id}\n")

        print("2. Testing User Retrieval...")
        user = user_manager.get_user("john_doe")
        print(f"   Retrieved user: {user}\n")

        print("3. Testing Feature Storage...")
        test_features = np.random.randn(26).astype(np.float32)
        feature_manager.store_feature("john_doe", test_features)
        feature_manager.store_feature("john_doe", test_features)
        print()

        print("4. Testing Feature Retrieval...")
        features = feature_manager.get_features_for_user("john_doe")
        print(f"   Retrieved {len(features)} features")
        print(f"   Feature shape: {features[0].shape}\n")

        print("5. Testing Command Logging...")
        command_logger.log_command("john_doe", "open notepad", "executed")
        print()

        print("6. Testing Command History...")
        history = command_logger.get_user_command_history("john_doe")
        print(f"   Retrieved {len(history)} commands\n")

        print("✓ Database operations test completed!")

    except Exception as e:
        print(f"✗ Test failed: {str(e)}", file=sys.stderr)
        sys.exit(1)
