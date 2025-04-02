from models.game_session import GameSession
from repositories.game_session import GameSessionRepository

class GameSessionTracker:
    """Utility for tracking game sessions without coupling games to repositories."""
    
    def __init__(self):
        """Initialize session tracker with repository."""
        self._repository = GameSessionRepository()
        self._active_session = None
    
    def start_session(self, user_id, game_id, difficulty_level="Medium"):
        """Start a new game session.
        
        Args:
            user_id (int): ID of the current user
            game_id (str): ID of the game being played
            difficulty_level (str): Selected difficulty level
            
        Returns:
            int: ID of the created session
        """
        # Create new session object
        self._active_session = GameSession(
            user_id=user_id,
            game_id=game_id,
            difficulty_level=difficulty_level
        )
        
        # Persist to database
        self._repository.create(self._active_session)
        return self._active_session.id
    
    def end_session(self, score=None, completed=True, session_data=None):
        """End the active game session.
        
        Args:
            score (int, optional): Final score for the session
            completed (bool): Whether the game completed successfully
            session_data (dict, optional): Any additional session data
            
        Returns:
            bool: True if session was successfully ended
        """
        if not self._active_session:
            return False
            
        # Update session data
        self._active_session.end(score, completed, session_data)
        
        # Persist to database
        result = self._repository.update(self._active_session)
        
        # Clear active session reference
        self._active_session = None
        
        return result
    
    def update_session_data(self, key, value):
        """Update a specific piece of session data during gameplay.
        
        Args:
            key (str): Data key to update
            value: Value to store
            
        Returns:
            bool: True if successful, False if no active session
        """
        if not self._active_session:
            return False
            
        self._active_session.session_data[key] = value
        return True
    
    def get_user_history(self, user_id, limit=10):
        """Get session history for a specific user.
        
        Args:
            user_id (int): User to get history for
            limit (int): Maximum number of sessions to return
            
        Returns:
            list: List of session objects
        """
        return self._repository.find_by_user(user_id, limit)
    
    @property
    def active_session_id(self):
        """Get ID of the current active session."""
        return self._active_session.id if self._active_session else None
