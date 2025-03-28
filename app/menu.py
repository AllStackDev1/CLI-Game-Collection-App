from auth.session import Session
from controllers import user as user_controller
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

def display_welcome():
    """Display welcome message."""
    console = Console()

    # Clear the screen for better presentation
    console.clear()

    # Display welcome header
    console.print(Panel("", title="Welcome to the Archive App", subtitle="Your ultimate CLI game collection"))


def display_menu(options):
    """
    Display a menu with numbered options.

    Args:
        title (str): The menu title
        options (list): List of option strings

    Returns:
        int: The selected option index (0-based)
    """
    console = Console()
    
    # Create menu table
    menu_table = Table(show_header=False, box=None, padding=(0, 2))
    menu_table.add_column(style="cyan")
    menu_table.add_column(style="white")

    # Add menu options
    for i, option in enumerate(options, 1):
        menu_table.add_row(f"{i}. {option}")
    
    # Display the menu
    console.print(menu_table)

    option_completer = WordCompleter(options, ignore_case=True)

    while True:
        try:
            choice = int(prompt("\nSelect an option: ", completer=option_completer))
            if 1 <= choice <= len(options):
                return choice - 1  # Convert to 0-based index
            print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")


def show_auth_menu():
    """Display authentication menu."""
    options = ["Login", "Register", "Exit"]
    choice = display_menu(options)

    if choice == 0:  # Login
        while True:
            user = user_controller.login_user()
            if user is False:
                continue
            return user
    elif choice == 1:  # Register
        return user_controller.register_user()
    else:  # Exit
        return None


def show_main_menu():
    """Display main application menu for authenticated users."""
    while True:
        user = Session.get_current_user()
        if not user:
            print("Error: No user logged in")
            return

        options = [
            "View My Profile",
            "Game Center",
            "Settings",
            "Logout",
            "Exit Application"
        ]

        choice = display_menu(options)

        if choice == 0:  # View Profile
            user_controller.display_user_profile()
            return True
        elif choice == 1:  # Game Center
            show_game_menu()
            return True
        elif choice == 2:  # Settings
            print("\nSettings menu is not implemented yet.")
            input("Press Enter to continue...")
            return True
        elif choice == 3:  # Logout
            user_controller.logout_user()
            return False
        elif choice == 4:  # Exit
            user_controller.logout_user()
            print("\nExiting application. Goodbye!")
            exit(0)


def show_game_menu():
    """Show game selection menu."""
    options = ["Game 1", "Game 2", "Back to Main Menu"]
    choice = display_menu(options)

    if choice == 0:  # Game 1
        print("\nGame 1 is not implemented yet.")
        input("Press Enter to continue...")
    elif choice == 1:  # Game 2
        print("\nGame 2 is not implemented yet.")
        input("Press Enter to continue...")
    # Choice 2 returns to main menu
