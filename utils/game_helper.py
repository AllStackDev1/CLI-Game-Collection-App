import os
import importlib
from rich.panel import Panel

from menu import show_post_game_options

def discover_games():
    """
    Discover and load available games from the games directory
    
    Returns:
        list: List of instantiated game objects
    """
    games = []
    games_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "games")
    
    # Create games directory if it doesn't exist
    if not os.path.exists(games_dir):
        os.makedirs(games_dir)
        return games
    
    # Look for game modules in the games directory
    for item in os.listdir(games_dir):
        game_dir = os.path.join(games_dir, item)
        
        # Check if it's a directory and contains a game.py file
        if os.path.isdir(game_dir) and os.path.exists(os.path.join(game_dir, "game.py")):
            try:
                # Dynamically import the game module
                module_path = f"games.{item}.game"
                game_module = importlib.import_module(module_path)
                
                # Look for a class that inherits from BaseGame
                for attr_name in dir(game_module):
                    attr = getattr(game_module, attr_name)
                    
                    # Check if it's a class and not BaseGame itself
                    if (isinstance(attr, type) and 
                        attr.__name__ != 'BaseGame' and
                        hasattr(attr, "__bases__") and
                        any('BaseGame' in str(base) for base in attr.__bases__)):
                        
                        # Create an instance of the game and add to list
                        game_instance = attr()
                        games.append(game_instance)
                        break
                        
            except Exception as e:
                print(f"Error loading game {item}: {str(e)}")
    
    return games


def run_game(game, user, console, session_tracker):
    """
    Run the selected game with appropriate UI feedback
    
    Args:
        game: The game instance to run
        user: The current user
        console: Rich console instance
        session_tracker: Session tracker instance
        
    Returns:
        str: Action to take next ("replay", "replay_new_diff", or None for returning to menu)
    """
    console.clear()
    
    info = game.get_info()
    
    # Display game header with selected difficulty
    console.print(Panel(
        f"[bold yellow]{info['name']}[/bold yellow]",
        border_style="yellow",
        subtitle=info["description"]
    ))
    
    console.print(f"[cyan]Difficulty:[/cyan] [bold]{game.difficulty}[/bold]")
    console.print("[green]Starting game...[/green]")
    
    try:
        # Start the game with the current user ID and session tracker
        game.start(user.id, session_tracker)
        
        # Game has finished, display the score
        console.print(f"\n[bold green]Game Over![/bold green]")
        console.print(f"[cyan]Your score:[/cyan] {game.score}")
        
        # Show high scores for this game
        show_high_scores(game.game_id, console, game.difficulty)
        
        # Present post-game options and handle user's choice
        return show_post_game_options(game, user, console, session_tracker)
        
    except Exception as e:
        console.print(f"[bold red]Error playing game:[/bold red] {str(e)}")
        console.print("\nPress Enter to return to the Games Menu...")
        input()
        return None


def select_difficulty_and_run_game(game, user, console, session_tracker):
    """
    Present difficulty options and run the selected game with chosen difficulty
    
    Args:
        game: The game instance to run
        user: The current user
        console: Rich console instance
        session_tracker: Session tracker instance
        
    Returns:
        str: "quit" if user chose to return to games menu
    """
    while True:  # Add loop to allow for replay options
        console.clear()
        
        game_info = game.get_info()
        
        # Display game information
        console.print(Panel(
            f"[bold yellow]{game_info['name']}[/bold yellow]",
            border_style="yellow",
            subtitle=game_info["description"]
        ))
        
        # Show difficulty selection menu
        console.print("\n[bold cyan]Select Difficulty:[/bold cyan]")
        
        difficulty_options = ["Easy", "Medium", "Hard", "Return to Games Menu"]
        
        # Display difficulty options and get user choice
        for i, option in enumerate(difficulty_options, 1):
            if option == "Return to Games Menu":
                console.print(f"  {i}. [dim]{option}[/dim]")
            elif option == game_info["difficulty"]:
                # Highlight the default difficulty
                console.print(f"  {i}. [green]{option}[/green] (Default)")
            else:
                console.print(f"  {i}. {option}")
        
        # Get user's difficulty selection
        valid_choices = [str(i) for i in range(1, len(difficulty_options) + 1)]
        choice = input("\nSelect an option (1-4): ")
        
        if choice not in valid_choices:
            console.print("[red]Invalid choice. Please try again.[/red]")
            console.print("\nPress Enter to continue...")
            input()
            continue
            
        choice = int(choice)
        
        # Check if the user wants to return to games menu
        if choice == len(difficulty_options):
            return "quit"
        
        # Set the selected difficulty on the game instance
        selected_difficulty = difficulty_options[choice - 1]
        game.difficulty = selected_difficulty
        
        # Run the game
        post_game_action = run_game(game, user, console, session_tracker)
        
        # Handle post-game choices
        if post_game_action == "replay":
            # Continue with same difficulty, just run the game again
            continue
        elif post_game_action == "replay_new_diff":
            # Loop back to difficulty selection
            continue
        else:
            # Return to games menu
            return "quit"


def show_high_scores(game_id, console):
    """
    Display high scores for a specific game
    
    Args:
        game_id: The ID of the game
        console: Rich console instance
    """
    # This is a placeholder - implement a proper high score service
    console.print("\n[bold cyan]High Scores[/bold cyan]")
    console.print("[yellow]High score functionality coming soon![/yellow]")