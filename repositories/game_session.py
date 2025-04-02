import json
from datetime import datetime
from models.game_session import GameSession
from db.connection import Database


class GameSessionRepository:
    """Repository for game session data access operations."""
    
    def create(self, game_session):
        """Insert a new game session record.
        
        Args:
            game_session (GameSession): Session object to persist
            
        Returns:
            int: ID of the created session
        """
        with Database.execute('''
        INSERT INTO game_sessions 
        (user_id, game_id, start_time, difficulty_level, session_data)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            game_session.user_id,
            game_session.game_id,
            game_session.start_time.isoformat(),
            game_session.difficulty_level,
            json.dumps(game_session.session_data)
        )) as cursor:
            game_session.id = cursor.lastrowid
            
            return game_session.id
    
    def update(self, game_session):
        """Update an existing game session.
        
        Args:
            game_session (GameSession): Session object with updated data
            
        Returns:
            bool: True if session was successfully updated
        """
        
        with Database.execute('''
        UPDATE game_sessions
        SET end_time = ?, duration = ?, score = ?, completed = ?, 
            difficulty_level = ?, session_data = ?
        WHERE id = ?
        ''', (
            game_session.end_time.isoformat() if game_session.end_time else None,
            game_session.duration,
            game_session.score,
            1 if game_session.completed else 0,
            game_session.difficulty_level,
            json.dumps(game_session.session_data),
            game_session.id
        )) as cursor:
        
            success = cursor.rowcount > 0
        
            return success
    
    def find_by_id(self, session_id):
        """Find a game session by its ID.
        
        Args:
            session_id (int): ID of the session to find
            
        Returns:
            GameSession: Session object if found, None otherwise
        """
        
        with Database.execute('''
        SELECT * FROM game_sessions WHERE id = ?
        ''', (session_id,)) as cursor:
        
            row = cursor.fetchone()
            
            if not row:
                return None
                
            return self._map_row_to_session(row)
    
    def find_by_user(self, user_id, limit=10):
        """Find recent sessions for a specific user.
        
        Args:
            user_id (int): User ID to search for
            limit (int): Maximum number of sessions to return
            
        Returns:
            list: List of GameSession objects
        """
        
        with Database.execute('''
        SELECT * FROM game_sessions 
        WHERE user_id = ? 
        ORDER BY start_time DESC 
        LIMIT ?
        ''', (user_id, limit)) as cursor:
        
            rows = cursor.fetchall()
            
            return [self._map_row_to_session(row) for row in rows]
    
    def _map_row_to_session(self, row):
        """Map a database row to a GameSession object.
        
        Args:
            row (sqlite3.Row): Database row
            
        Returns:
            GameSession: Populated session object
        """
        session_data = {}
        if row['session_data']:
            try:
                session_data = json.loads(row['session_data'])
            except json.JSONDecodeError:
                session_data = {}
        
        return GameSession(
            id=row['id'],
            user_id=row['user_id'],
            game_id=row['game_id'],
            start_time=datetime.fromisoformat(row['start_time']) if row['start_time'] else None,
            end_time=datetime.fromisoformat(row['end_time']) if row['end_time'] else None,
            duration=row['duration'],
            score=row['score'],
            completed=bool(row['completed']),
            difficulty_level=row['difficulty_level'],
            session_data=session_data
        )