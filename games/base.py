from datetime import time


class BaseGame:
    """Base class that all games in the collection should inherit from."""
    
    def __init__(self, game_id, name, description, difficulty="Medium"):
        """Initialize the base game with common properties.
        
        Args:
            game_id (str): Unique identifier for the game
            name (str): The name of the game
            description (str): A short description of the game
            difficulty (str): Game difficulty level (Easy, Medium, Hard)
        """
        self.game_id = game_id
        self.name = name
        self.description = description
        self.difficulty = difficulty
        self.score = 0  # Current game score
        self.is_running = False
        self.session = None
        
        # Basic metrics tracking
        self.start_time = None
        self.attempts = 0
    
    def start(self, user_id, session_tracker=None):
        """Set up and start the game."""
        # Reset game state and metrics
        self.score = 0
        self.attempts = 0
        self.is_running = True
        
        # Start timing
        self.start_time = time.time()
        
        # Track session if tracker is provided
        self.session = session_tracker
        if self.session:
            self.session.start_session(user_id, self.game_id, self.difficulty)
            # Initialize metrics
            self._update_metrics()
        
        # Configure game based on difficulty before setup
        self.configure_difficulty()
        
        # Game-specific setup and run
        self.setup()
        self.run()
    
    def configure_difficulty(self):
        """
        Configure game parameters based on selected difficulty.
        Child classes should override this to implement difficulty-specific settings.
        """
        pass
    
    def setup(self):
        """Set up the game environment before running.
        Should be implemented by child classes."""
        raise NotImplementedError("Game classes must implement setup method")
    
    def run(self):
        """Main game loop.
        Should be implemented by child classes."""
        raise NotImplementedError("Game classes must implement run method")
    
    def stop(self, completed=True, session_data=None):
        """Stop the game and perform cleanup.
        
        Args:
            completed (bool): Whether the game completed successfully
            session_data (dict, optional): Any additional session data
        
        Returns:
            int: The final score from the game session
        """

        # Track session end using the internal score
        if self.session:
            self.session.end_session(self.score, completed, session_data)
        
        self.is_running = False
        self.cleanup()
        
        # Return the final score for external use
        return self.score
    
    def update_score(self, points):
        """Update the current game score.
        
        Args:
            points (int): Points to add to the current score (can be negative)
        
        Returns:
            int: The updated score
        """
        self.score += points
        
        # Track progress if session tracker is available
        if self.session:
            self.session.update_session_data('score', self.score)
            
        return self.score
    
    def track_progress(self, key, value):
        """Update session data during gameplay.
        
        Args:
            key (str): Key identifying the type of data
            value: The value to record
        """
        if self.session:
            self.session.update_session_data(key, value)
    
    def cleanup(self):
        """Clean up any resources. Can be overridden by child classes."""
        pass

    def get_info(self):
        """Return a dictionary with game information."""
        return {
            "game_id": self.game_id,
            "name": self.name,
            "description": self.description,
            "difficulty": self.difficulty
        }

# def update_highscore(self, player_name, score):
#     """Update high score if the current score is higher.
    
#     Args:
#         player_name: Name of the player
#         score: Player's score to compare with existing high scores
    
#     Returns:
#         bool: True if it's a new high score, False otherwise
#     """
#     if player_name not in self.highscores or score > self.highscores[player_name]:
#         self.highscores[player_name] = score
#         return True
#     return False

# def display_highscores(self):
#     """Display the high scores for this game."""
#     from rich.table import Table
    
#     table = Table(title=f"{self.name} High Scores")
#     table.add_column("Player")
#     table.add_column("Score")
    
#     # Sort high scores in descending order
#     sorted_scores = sorted(
#         self.highscores.items(), 
#         key=lambda x: x[1], 
#         reverse=True
#     )
    
#     for player, score in sorted_scores:
#         table.add_row(player, str(score))
        
#     self.console.print(table)

# def display_title(self):
#     """Display the game title and description."""
#     # Subclasses can override for custom styling
#     from rich.panel import Panel
#     from rich.text import Text
#     import pyfiglet
    
#     title_art = pyfiglet.figlet_format(self.name, font="small")
#     title_text = Text(title_art, style="bold blue")
#     self.console.print(Panel(title_text))
#     self.console.print(Panel(self.description, style="green"))

# def display_instructions(self):
#     """Display game instructions to the player."""
#     # Subclasses should override this
#     self.console.print("[yellow]No instructions provided for this game.[/yellow]")
