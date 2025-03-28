def up():
    """Create the schema_migrations table to track applied migrations."""
    return """
    CREATE TABLE IF NOT EXISTS schema_migrations (
        version INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """


def down():
    """Remove the schema_migrations table."""
    return """
    DROP TABLE IF EXISTS schema_migrations;
    """