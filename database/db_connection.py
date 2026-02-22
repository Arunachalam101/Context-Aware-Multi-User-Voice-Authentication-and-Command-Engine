"""
Database connection module for Voice Authentication Engine.

Handles SQLite database connections, initialization, and schema creation.
All database operations should use the connection provided by this module.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
import sys

# Import configuration
from utils.config import (
    DATABASE_FILE,
    CREATE_USERS_TABLE,
    CREATE_VOICE_FEATURES_TABLE,
    CREATE_COMMAND_LOGS_TABLE,
    create_directories,
)


class DatabaseConnectionError(Exception):
    """Raised when database connection fails."""

    pass


class DatabaseInitializationError(Exception):
    """Raised when database initialization fails."""

    pass


class DatabaseConnection:
    """
    Manages SQLite database connections for the voice authentication system.

    This class provides methods to:
    - Connect to the SQLite database
    - Initialize database schema (create tables)
    - Execute queries safely with context management
    - Handle connection pooling and cleanup
    """

    _instance = None
    """Singleton instance of the database connection."""

    def __init__(self, db_path=None):
        """
        Initialize database connection.

        Args:
            db_path (Path or str, optional): Path to the SQLite database file.
                                           Defaults to DATABASE_FILE from config.

        Raises:
            DatabaseConnectionError: If connection cannot be established.
        """
        if db_path is None:
            db_path = DATABASE_FILE

        self.db_path = Path(db_path)
        self.connection = None

        try:
            self.connect()
            print(f"[OK] Database connection established: {self.db_path}")
        except Exception as e:
            raise DatabaseConnectionError(
                f"Failed to connect to database at {self.db_path}: {str(e)}"
            )

    def connect(self):
        """
        Establish connection to SQLite database.

        Creates database file if it doesn't exist.
        """
        # Ensure database directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        # Enable foreign keys
        self.connection.execute("PRAGMA foreign_keys = ON")

    def disconnect(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            print(f"✓ Database connection closed")

    def initialize_schema(self):
        """
        Create all required database tables.

        Executes the following SQL statements:
        - CREATE_USERS_TABLE
        - CREATE_VOICE_FEATURES_TABLE
        - CREATE_COMMAND_LOGS_TABLE

        Raises:
            DatabaseInitializationError: If table creation fails.
        """
        if not self.connection:
            raise DatabaseInitializationError("No active database connection")

        try:
            cursor = self.connection.cursor()

            # Create tables
            cursor.execute(CREATE_USERS_TABLE)
            print("[OK] Created 'users' table")

            cursor.execute(CREATE_VOICE_FEATURES_TABLE)
            print("[OK] Created 'voice_features' table")

            cursor.execute(CREATE_COMMAND_LOGS_TABLE)
            print("[OK] Created 'command_logs' table")

            self.connection.commit()
            print("[OK] Database schema initialized successfully")

        except sqlite3.Error as e:
            self.connection.rollback()
            raise DatabaseInitializationError(f"Failed to initialize schema: {str(e)}")

    @contextmanager
    def cursor(self):
        """
        Context manager for database cursor.

        Yields a database cursor and automatically commits or rolls back
        based on whether an exception occurred.

        Yields:
            sqlite3.Cursor: Database cursor for executing queries.

        Example:
            with db_connection.cursor() as cur:
                cur.execute("SELECT * FROM users")
                rows = cur.fetchall()
        """
        try:
            cur = self.connection.cursor()
            yield cur
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Database operation failed: {str(e)}")

    def execute_query(self, query, params=None):
        """
        Execute a SELECT query and return results.

        Args:
            query (str): SQL SELECT query to execute.
            params (tuple, optional): Parameters to use in the query.

        Returns:
            list: List of rows as sqlite3.Row objects.

        Raises:
            DatabaseError: If query execution fails.
        """
        try:
            with self.cursor() as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                return cur.fetchall()
        except Exception as e:
            raise DatabaseError(f"Query execution failed: {str(e)}")

    def execute_update(self, query, params=None):
        """
        Execute an INSERT, UPDATE, or DELETE query.

        Args:
            query (str): SQL INSERT/UPDATE/DELETE query to execute.
            params (tuple, optional): Parameters to use in the query.

        Returns:
            int: Number of rows affected by the query.

        Raises:
            DatabaseError: If query execution fails.
        """
        try:
            with self.cursor() as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                return cur.rowcount
        except Exception as e:
            raise DatabaseError(f"Update execution failed: {str(e)}")

    def execute_insert(self, query, params=None):
        """
        Execute an INSERT query and return the inserted row ID.

        Args:
            query (str): SQL INSERT query to execute.
            params (tuple, optional): Parameters to use in the query.

        Returns:
            int: The ID of the last inserted row.

        Raises:
            DatabaseError: If query execution fails.
        """
        try:
            with self.cursor() as cur:
                if params:
                    cur.execute(query, params)
                else:
                    cur.execute(query)
                return cur.lastrowid
        except Exception as e:
            raise DatabaseError(f"Insert execution failed: {str(e)}")

    def table_exists(self, table_name):
        """
        Check if a table exists in the database.

        Args:
            table_name (str): Name of the table to check.

        Returns:
            bool: True if table exists, False otherwise.
        """
        try:
            query = (
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
            )
            result = self.execute_query(query, (table_name,))
            return len(result) > 0
        except Exception:
            return False

    def get_connection(self):
        """
        Get the underlying SQLite connection object.

        Returns:
            sqlite3.Connection: The SQLite connection object.
        """
        return self.connection

    @classmethod
    def get_instance(cls, db_path=None):
        """
        Get or create singleton instance of DatabaseConnection.

        Args:
            db_path (Path or str, optional): Path to database file.

        Returns:
            DatabaseConnection: Singleton instance.
        """
        if cls._instance is None:
            cls._instance = cls(db_path)
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance (useful for testing)."""
        if cls._instance:
            cls._instance.disconnect()
            cls._instance = None


class DatabaseError(Exception):
    """Generic database error."""

    pass


def init_database(db_path=None):
    """
    Initialize the database with schema and return connection.

    This is the main entry point for database initialization.

    Args:
        db_path (Path or str, optional): Path to database file.

    Returns:
        DatabaseConnection: Initialized database connection.

    Raises:
        DatabaseError: If initialization fails.
    """
    try:
        # Create required directories
        create_directories()

        # Create or get connection
        db_connection = DatabaseConnection(db_path)

        # Initialize schema
        db_connection.initialize_schema()

        print("\n[OK] Database initialized successfully!")
        return db_connection

    except (DatabaseConnectionError, DatabaseInitializationError) as e:
        print(f"\n✗ Database initialization failed: {str(e)}", file=sys.stderr)
        raise


if __name__ == "__main__":
    # When run directly, initialize the database
    print("\n" + "=" * 70)
    print("Voice Authentication Engine - Database Initialization")
    print("=" * 70 + "\n")

    try:
        db = init_database()
        print("\n" + "=" * 70)
        print("Database initialization completed successfully!")
        print("=" * 70 + "\n")
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"Initialization failed: {str(e)}")
        print("=" * 70 + "\n")
        sys.exit(1)
