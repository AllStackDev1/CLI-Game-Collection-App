def up(cursor):
    """Create game_sessions table."""
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        game_id TEXT NOT NULL,
        start_time TIMESTAMP NOT NULL,
        end_time TIMESTAMP,
        duration INTEGER,
        score INTEGER,
        completed INTEGER DEFAULT 0,
        difficulty_level TEXT,
        session_data TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    # Create an index on user_id for faster queries
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_game_sessions_user_id ON game_sessions(user_id)')


def down(cursor):
    """Drop game_sessions table."""
    cursor.execute('DROP TABLE IF EXISTS game_sessions')
    cursor.execute('DROP INDEX IF EXISTS idx_game_sessions_user_id')