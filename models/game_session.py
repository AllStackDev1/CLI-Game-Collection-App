from datetime import datetime

class GameSession:
    """Model representing a game play session."""
    
    def __init__(self, id=None, user_id=None, game_id=None, start_time=None, 
                end_time=None, duration=None, score=None, completed=False, 
                difficulty_level="Medium", session_data=None):
        """Initialize a game session instance.
        
        Args:
            id (int, optional): Primary key of the session
            user_id (int): Foreign key to the users table
            game_id (str): Identifier for the game that was played
            start_time (datetime, optional): When the session started
            end_time (datetime, optional): When the session ended
            duration (int, optional): Total play duration in seconds
            score (int, optional): Final score achieved
            completed (bool): Whether the game was completed or abandoned
            difficulty_level (str): The difficulty level the game was played at
            session_data (dict, optional): Additional game-specific session data
        """
        self.id = id
        self.user_id = user_id
        self.game_id = game_id
        self.start_time = start_time or datetime.now()
        self.end_time = end_time
        self.duration = duration
        self.score = score
        self.completed = completed
        self.difficulty_level = difficulty_level
        self.session_data = session_data or {}
    
    def end(self, score=None, completed=True, session_data=None):
        """End the current session and calculate duration.
        
        Args:
            score (int, optional): Final score to record
            completed (bool): Whether the game was completed successfully
            session_data (dict, optional): Additional game-specific data to store
        """
        self.end_time = datetime.now()
        self.duration = (self.end_time - self.start_time).total_seconds()
        self.score = score
        self.completed = completed
        
        if session_data:
            self.session_data.update(session_data)
    
    def to_dict(self):
        """Convert session to dictionary representation."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'game_id': self.game_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration': self.duration,
            'score': self.score,
            'completed': self.completed,
            'difficulty_level': self.difficulty_level,
            'session_data': self.session_data
        }