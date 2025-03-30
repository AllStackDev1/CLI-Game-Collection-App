from rich.console import Console
from rich.panel import Panel

class BaseGame:
    """Base class for all games in the collection"""
    
    def __init__(self, name, description):
        """
        Initialize a game with name and description
        
        Args:
            name (str): The name of the game
            description (str): A short description of the game
        """
        self.name = name
        self.description = description
    
    def display_info(self, console=None):
        """
        Display game information
        
        Args:
            console (Console, optional): Rich console for display
        """
        if console is None:
            console = Console()
            
        console.print(Panel(
            f"[bold]{self.name}[/bold]\n\n{self.description}",
            border_style="green"
        ))
    
    def play(self, user=None):
        """
        Play the game (to be implemented by subclasses)
        
        Args:
            user (dict, optional): Current user data
        
        Returns:
            dict: Game results
        """
        raise NotImplementedError("Each game must implement its own play method")

