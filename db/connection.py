import sqlite3
from pathlib import Path
from contextlib import contextmanager


class Database:
    """Database connection manager with class methods for migration and general use."""

    _db_path = None
    _connection = None

    @classmethod
    def initialize(cls, db_name="archive.db"):
        """Initialize the database path."""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        cls._db_path = data_dir / db_name

    @classmethod
    def _connect(cls):
        """Establish a database connection with optimized settings."""
        if cls._db_path is None:
            cls.initialize()

        if cls._connection is None:
            cls._connection = sqlite3.connect(
                cls._db_path,
                timeout=30,  # Increased timeout for write operations
                isolation_level=None  # Auto-commit mode
            )
            # Enable Write-Ahead Logging for better performance
            cls._connection.execute("PRAGMA journal_mode=WAL;")

        return cls._connection

    @classmethod
    @contextmanager
    def execute(cls, query, params=None):
        """
        Context-managed method for database operations.

        Args:
            query (str): SQL query to execute
            params (tuple, optional): Query parameters

        Yields:
            sqlite3.Cursor: Cursor for database operations
        """
        connection = None
        cursor = None
        try:
            # Establish connection
            connection = cls._connect()
            cursor = connection.cursor()

            # Print debug information
            print(f"[DB] Executing query: {query} | Params: {params}")

            # Execute query with optional parameters
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Commit for write operations
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP')):
                connection.commit()

            yield cursor

        except sqlite3.OperationalError as e:
            # Handle potential lock errors
            print(f"[DB] Database error: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            # Ensure cursor and connection are closed
            if cursor:
                cursor.close()

    @classmethod
    def execute_script(cls, script):
        """
        Execute a SQL script with multiple statements for migrations.

        Args:
            script (str): SQL script to execute
        """
        try:
            # Establish connection
            connection = cls._connect()

            print("[DB] Executing migration script...")
            connection.executescript(script)
            connection.commit()

        except sqlite3.OperationalError as e:
            print(f"[DB] Migration script error: {e}")
            if cls._connection:
                cls._connection.rollback()
            raise

    @classmethod
    def close(cls):
        """Close the database connection."""
        if cls._connection:
            cls._connection.close()
            cls._connection = None

