import datetime
import random
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit.shortcuts import confirm

from base import BaseGame

class NumberGuessingGame(BaseGame):
    """A simple number guessing game where the player tries to 
    guess a randomly generated number within a limited number of attempts."""
    
    def __init__(self):
        """Initialize the Number Guessing Game with default settings."""
        super().__init__(
            game_id="number_guessing",
            name="Number Guessing Game",
            description="Guess the secret number within the given range and attempts",
            difficulty="Medium"  # Default difficulty
        )
        
        # Default game parameters will be set in configure_difficulty
        self.min_number = None
        self.max_number = None
        self.max_attempts = None
        self.secret_number = None
        self.attempts_made = 0
        self.guesses = []
        self.console = Console()
        
    def configure_difficulty(self):
        """Configure game parameters based on the selected difficulty level."""
        # Set game parameters based on difficulty
        if self.difficulty == "Easy":
            self.min_number = 1
            self.max_number = 50
            self.max_attempts = 10
        elif self.difficulty == "Medium":
            self.min_number = 1
            self.max_number = 100
            self.max_attempts = 7
        elif self.difficulty == "Hard":
            self.min_number = 1
            self.max_number = 200
            self.max_attempts = 5
        else:
            # Fallback to Medium if an unknown difficulty is provided
            self.min_number = 1
            self.max_number = 100
            self.max_attempts = 7
            
        # Record difficulty parameters as metrics
        if self.session:
            self.track_progress("difficulty_settings", {
                "min_number": self.min_number,
                "max_number": self.max_number,
                "max_attempts": self.max_attempts
            })
            
    def setup(self):
        """Set up the game by generating a random secret number."""
        # Reset game state
        self.attempts_made = 0
        self.guesses = []
        self.secret_number = random.randint(self.min_number, self.max_number)
        
        # Record initial game parameters as metrics
        self.record_metric("range", f"{self.min_number}-{self.max_number}")
        self.record_metric("max_attempts", self.max_attempts)
    
    def record_metric(self, key, value):
        """Helper method to record game metrics."""
        if self.session:
            self.track_progress(key, value)
    
    def run(self):
        """Run the main game loop."""
        try:
            self.display_welcome()
            
            while self.is_running and self.attempts_made < self.max_attempts:
                # Get player's guess
                guess = self.get_player_guess()
                
                # Handle player quitting
                if guess is None:
                    return self.handle_quit()
                
                # Process the guess
                result = self.process_guess(guess)
                
                # Check if player won
                if result == "correct":
                    self.handle_victory()
                    break
                    
                # Update attempts count
                self.attempts_made += 1
                
                # Check if player lost (used all attempts)
                if self.attempts_made >= self.max_attempts:
                    self.handle_defeat()
        except KeyboardInterrupt:
            # Final fallback for Ctrl+C if it bubbles up here
            self.console.print("\n[yellow]Game forcefully interrupted.[/yellow]")
            return self.stop(completed=False)
        
        except Exception as e:
            # Handle unexpected errors, ensuring we stop the game properly
            self.console.print(f"\n[red]An error occurred: {str(e)}[/red]")
            return self.stop(completed=False)
        
    def display_welcome(self):
        """Display welcome message and instructions."""
        title = Text("🎲 NUMBER GUESSING GAME 🎲", style="bold blue")
        difficulty_text = f"[bold]{self.difficulty}[/bold] Difficulty"
        instructions = (
            f"I'm thinking of a number between {self.min_number} and {self.max_number}.\n"
            f"You have {self.max_attempts} attempts to guess it correctly."
        )
        self.console.print(Panel(
            instructions, 
            title=title, 
            subtitle=difficulty_text,
            border_style="green"
        ))
    
    def get_player_guess(self):
        """Get and validate a guess from the player with timing and quit option."""
        attempts_left = self.max_attempts - self.attempts_made
        prompt_text = f"Attempt {self.attempts_made + 1}/{self.max_attempts}: Enter your guess (or 'q' to quit)"
        
        guess_start_time = datetime.datetime.now().timestamp()
        
        while True:
            try:
                # Get input as a string first to check for quit command
                input_value = input(prompt_text + ": ")
                
                # Check for quit command
                if input_value.lower() == 'q':
                    if self._confirm_quit():
                        return None
                    else:
                        # Player changed their mind, restart the timer
                        guess_start_time = datetime.datetime.now().timestamp()
                        continue
                
                # Parse as integer
                guess = int(input_value)
                
                # Validate guess is in range
                if guess < self.min_number or guess > self.max_number:
                    self.console.print(
                        f"[red]Please enter a number between {self.min_number} and {self.max_number}.[/red]"
                    )
                    continue
                
                # Calculate time taken for this guess
                guess_time = datetime.datetime.now().timestamp() - guess_start_time
                
                # Add to guesses history
                self.guesses.append(guess)
                
                # Record metrics for this guess
                self.record_metric(f"guess_{self.attempts_made + 1}", {
                    "value": guess,
                    "time_taken": round(guess_time, 2)
                })
                
                # Update attempts count for metrics
                self.log_attempt()
                
                return guess
            except ValueError:
                if input_value.lower() != 'q':  # Only show error if it wasn't a quit attempt
                    self.console.print("[red]Please enter a valid number.[/red]")
            except KeyboardInterrupt:
                # Handle Ctrl+C interruption
                self.console.print("\n[yellow]Game interrupted. Would you like to quit?[/yellow]")
                if self._confirm_quit():
                    return None
                else:
                    # Restart the timer
                    guess_start_time = datetime.datetime.now().timestamp()
    
    def process_guess(self, guess):
        """Process the player's guess and provide feedback."""
        if guess < self.secret_number:
            self.console.print("[yellow]Too low! Try a higher number.[/yellow]")
            return "higher"
        elif guess > self.secret_number:
            self.console.print("[yellow]Too high! Try a lower number.[/yellow]")
            return "lower"
        else:
            return "correct"
    
    def handle_victory(self):
        """Handle player victory."""
        attempts_used = self.attempts_made + 1
        
        # Calculate score based on difficulty
        score = self.calculate_score(attempts_used)
        
        # Update the base class score
        self.score = score
        
        # Record final game stats
        self.record_metric("attempts_used", attempts_used)
        self.record_metric("success", True)
        
        # Show victory message
        message = (
            f"\n[bold green]🎉 Congratulations! 🎉[/bold green]\n"
            f"You guessed the correct number [bold]{self.secret_number}[/bold] "
            f"in [bold]{attempts_used}[/bold] attempts.\n"
            f"Your score: [bold]{score}[/bold] points"
        )
        self.console.print(Panel(message, border_style="green"))
        
        # Stop game
        self.stop(completed=True)
    
    def calculate_score(self, attempts_used):
        """Calculate score based on difficulty level and attempts used."""
        # Base score calculations
        max_possible_score = 1000
        attempts_factor = (self.max_attempts - attempts_used + 1) / self.max_attempts
        range_size = self.max_number - self.min_number + 1
        
        # Difficulty multipliers
        if self.difficulty == "Easy":
            difficulty_multiplier = 1.0
        elif self.difficulty == "Medium":
            difficulty_multiplier = 1.5
        elif self.difficulty == "Hard":
            difficulty_multiplier = 2.0
        else:
            difficulty_multiplier = 1.0
            
        # Calculate final score: More attempts left = higher score
        # Wider number range = higher score
        # Higher difficulty = higher score multiplier
        base_score = max_possible_score * attempts_factor
        adjusted_score = base_score * (range_size / 100) * difficulty_multiplier
        
        return int(adjusted_score)
    
    def handle_defeat(self):
        """Handle player defeat (ran out of attempts)."""
        # Record final game stats
        self.record_metric("attempts_used", self.max_attempts)
        self.record_metric("success", False)
        
        # Set score to 0 for defeat
        self.score = 0
        
        # Show defeat message
        message = (
            f"\n[bold red]Game Over[/bold red]\n"
            f"You've used all {self.max_attempts} attempts.\n"
            f"The secret number was [bold]{self.secret_number}[/bold]."
        )
        self.console.print(Panel(message, border_style="red"))
        
        # Stop game
        self.stop(completed=True)
    
    def _confirm_quit(self):
        """Confirm if the player wants to quit."""
        try:
            self.console.print("[yellow]Are you sure you want to quit the game?[/yellow]")
            return confirm("Quit game?")
        except KeyboardInterrupt:
            # If they press Ctrl+C during confirmation, interpret as Yes
            return True
    
    def handle_quit(self):
        """Handle player quitting the game voluntarily."""
        # Record metrics about the quit
        self.record_metric("quit_early", True)
        self.record_metric("attempts_before_quit", len(self.guesses))
        
        # Show quit message
        message = (
            f"\n[yellow]Game ended early.[/yellow]\n"
            f"You used {len(self.guesses)} out of {self.max_attempts} attempts.\n"
            f"The secret number was [bold]{self.secret_number}[/bold]."
        )
        self.console.print(Panel(message, border_style="yellow"))
        
        # Stop game with incomplete status
        return self.stop(completed=False)
    
    def cleanup(self):
        """Perform any cleanup needed after the game ends."""
        pass