from auth.session import Session
from controllers import user as user_controller
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter


def display_menu(options, user = None):
    """
    A dynamic menu function that displays menu options and user details at the top if user is in session

    Args:
        options (list): List of option strings
        user (User|None): user object

    Returns:
        int: The selected option index (1-based)
    """
    console = Console()

    # Clear the screen for better presentation
    console.clear()

    # Display user information if available
    if user:
        # Create a header with user information
        console.print(Panel(
            f"[bold green]Welcome, {user['name']}![/bold green]\n\n"
            f"Email: {user['email']}",
            title="[bold]CLI Game Collection[/bold]",
            subtitle="[bold]Main Menu[/bold]",
            border_style="blue"
        ))
    else:
        console.print(Panel("Ultimate CLI game collection", title="[bold]Welcome to the Archive[/bold]", subtitle="[bold]Main Menu[/bold]"))
    
    # Create menu table with options
    menu_grid = Table.grid(padding=(0, 0))
    menu_grid.add_column(style="cyan")
    menu_grid.add_column(style="white")

    # Add menu options
    choice_strings = []
    for i, option in enumerate(options, 1):
        menu_grid.add_row(f"{i}. {option}")
        choice_strings.append(str(i))
    
    # Display the menu
    console.print(menu_grid)

    # Horizontal line to visually separate the menu from input area
    console.print("─" * console.width)

    option_completer = WordCompleter(choice_strings, ignore_case=True)

    while True:
        try:
            choice = prompt("\nSelect an option: ", completer=option_completer)
            if choice in choice_strings:
                return int(choice)
            console.print(f"[red]Please enter a number between 1 and {len(options)}[/red]")
        except ValueError:
            console.print("[red]Please enter a valid number[/red]")


def show_auth_menu():
    """Display authentication menu."""
    options = ["Login", "Register", "Exit"]
    choice = display_menu(options)

    if choice == 1:  # Login
        while True:
            user = user_controller.login_user()
            if user is False:
                continue
            return user
    elif choice == 2:  # Register
        return user_controller.register_user()
    else:  # Exit
        return None


def display_user_profile(user=None):
    """
    Display detailed user profile information and allow returning to main menu.
    
    Returns:
        bool: Always returns True to continue the session
    """
    console = Console()
    console.clear()
    
    # Create a detailed profile panel
    profile_items = [
        ("Username", user.get('username', 'N/A')),
        ("Name", user.get('name', 'N/A')),
        ("Email", user.get('email', 'N/A')),
        ("Account Created", user.get('created_at', 'N/A')),
        ("Last Login", user.get('last_login', 'N/A'))
    ]
    
    # Additional profile data, if available
    # if 'high_scores' in user and user['high_scores']:
    #     top_scores = []
    #     for game, score in user['high_scores'].items():
    #         top_scores.append(f"• {game}: {score} points")
        
    #     if top_scores:
    #         profile_items.append(("Top Scores", "\n".join(top_scores)))
    
    # Create and display profile grid
    profile_grid = Table.grid(padding=(0, 2))
    profile_grid.add_column(style="bold cyan", justify="right")
    profile_grid.add_column(style="white")
    
    for label, value in profile_items:
        profile_grid.add_row(f"{label}:", value)
    
    console.print(Panel(
        profile_grid,
        title="[bold]User Profile[/bold]",
        border_style="green",
        padding=(1, 2)
    ))
    
    console.print(Panel("1. Return to Main Menu", title="Options", border_style="blue"))
    console.print("\nPress Enter to return to the main menu...")
    
    # Simple input - just waiting for user to acknowledge
    input()
    return True


def show_edit_profile_screen(current_user):
    """
    Display the user profile editing interface
    Args:
        current_user (User): user object
    
    Returns:
        bool: True to keep session active, False otherwise
    """
    console = Console()
    console.clear()
    
    console.print(Panel("[bold]Edit Your Profile[/bold]", border_style="blue"))
    
    # Display current information
    console.print("\n[cyan]Current Profile Information:[/cyan]")
    console.print(f"Name: {current_user.get('name', 'Not set')}")
    console.print(f"Email: {current_user.get('email', 'Not set')}")
    
    # Collect new information
    console.print("\n[yellow]Enter new information (leave blank to keep current value):[/yellow]")
    
    new_name = prompt(f"Name [{current_user.get('name', '')}]: ") or current_user.get('name', '')
    new_email = prompt(f"Email [{current_user.get('email', '')}]: ") or current_user.get('email', '')
    
    # Password is special - never display the current one
    console.print("\n[yellow]Change Password (leave blank to keep current):[/yellow]")
    new_password = prompt("New Password: ", is_password=True)
    
    # Only ask for confirmation if a new password was entered
    confirm_password = ""
    if new_password:
        confirm_password = prompt("Confirm Password: ", is_password=True)
    
    # Confirm changes
    console.print("\n[yellow]Review your changes:[/yellow]")
    console.print(f"Name: {current_user.get('name', '')} -> {new_name}")
    console.print(f"Email: {current_user.get('email', '')} -> {new_email}")
    console.print(f"Password: {'*****' if new_password else 'Unchanged'}")
    
    # Ask for confirmation
    confirmation = prompt("\nConfirm these changes? (y/n): ").lower()
    if confirmation != 'y':
        console.print("[yellow]Profile update canceled.[/yellow]")
        return True
    
    # Build update data
    update_data = {
        'name': new_name,
        'email': new_email
    }
    
    # Only include password if it was changed
    if new_password:
        update_data['password'] = new_password
        update_data['confirm_password'] = confirm_password
    
    # Call controller to update user
    success, message = user_controller.update_user_details(update_data)
    
    # Display result
    if success:
        console.print(f"[green]{message}[/green]")
    else:
        console.print(f"[red]Error: {message}[/red]")
    
    # Wait for user acknowledgment
    console.print("\nPress Enter to continue...")
    input()
    
    return True


def show_delete_account_screen():
    """
    Display the account deletion confirmation screen
    
    Returns:
        bool: False if account was deleted, True otherwise
    """
    console = Console()
    console.clear()
    
    # Get current user
    current_user = Session.get_current_user()
    if not current_user:
        console.print("[red]Error: No active user session[/red]")
        return True
    
    # Create a warning panel
    console.print(Panel(
        "[bold red]⚠️  ACCOUNT DELETION WARNING ⚠️[/bold red]\n\n"
        "This action will permanently delete your account and all associated data.\n"
        "This cannot be undone.",
        title="Delete Account",
        border_style="red",
        padding=(1, 2)
    ))
    
    # Initial confirmation
    console.print("\n[yellow]Please type DELETE to confirm you want to delete your account:[/yellow]")
    confirmation = prompt("> ")
    
    if confirmation.upper() != "DELETE":
        console.print("[green]Account deletion cancelled.[/green]")
        console.print("\nPress Enter to return to the main menu...")
        input()
        return True
    
    # Secondary confirmation with password
    console.print("\n[yellow]For security, please enter your password:[/yellow]")
    password = prompt("> ", is_password=True)
    
    if not password:
        console.print("[green]Account deletion cancelled.[/green]")
        console.print("\nPress Enter to return to the main menu...")
        input()
        return True
    
    # Final warning
    console.print("\n[bold red]WARNING: This is your last chance to cancel![/bold red]")
    console.print("[yellow]Are you absolutely sure you want to delete your account? (yes/no)[/yellow]")
    final_confirmation = prompt("> ").lower()
    
    if final_confirmation != "yes":
        console.print("[green]Account deletion cancelled.[/green]")
        console.print("\nPress Enter to return to the main menu...")
        input()
        return True
    
    # Proceed with account deletion
    console.print("\n[yellow]Deleting your account...[/yellow]")
    
    success, message = user_controller.delete_current_user_account(password)
    
    if success:
        console.print(f"[green]{message}[/green]")
        console.print("\n[yellow]You will be logged out. Press Enter to continue...[/yellow]")
        input()
        return False  # Return False to indicate session should end
    else:
        console.print(f"[red]Error: {message}[/red]")
        console.print("\nPress Enter to return to the main menu...")
        input()
        return True  # Return True to keep session active


def show_games_menu():
    """
    Display the games menu with placeholder game options
    
    Returns:
        bool: True to continue the session
    """
    console = Console()
    
    while True:
        console.clear()
        
        # Get current user
        user = Session.get_current_user()
        if not user:
            console.print("[red]Error: No active user session[/red]")
            return True
        
        # Display game menu header
        console.print(Panel(
            "[bold cyan]Game Collection[/bold cyan]",
            border_style="green",
            subtitle="Choose a game to play"
        ))
        
        # Define game options
        game_options = [
            "Game 1 - Placeholder",
            "Game 2 - Placeholder",
            "Game 3 - Placeholder",
            "Return to Main Menu"
        ]
        
        # Display menu and get user choice
        choice = display_menu(game_options, user)
        
        if choice == 1:  # Game 1
            console.clear()
            console.print(Panel(
                "[bold yellow]Game 1[/bold yellow]\n\nThis game is not yet implemented.",
                border_style="yellow"
            ))
            console.print("\nPress Enter to return to the Games Menu...")
            input()
            
        elif choice == 2:  # Game 2
            console.clear()
            console.print(Panel(
                "[bold yellow]Game 2[/bold yellow]\n\nThis game is not yet implemented.",
                border_style="yellow"
            ))
            console.print("\nPress Enter to return to the Games Menu...")
            input()
            
        elif choice == 3:  # Game 3
            console.clear()
            console.print(Panel(
                "[bold yellow]Game 3[/bold yellow]\n\nThis game is not yet implemented.",
                border_style="yellow"
            ))
            console.print("\nPress Enter to return to the Games Menu...")
            input()
            
        elif choice == 4:  # Return to Main Menu
            return True


def show_main_menu():
    """Display main application menu for authenticated users."""
    while True:
        user = Session.get_current_user()
        if not user:
            print("Error: No user logged in")
            return

        options = [
            "Games",
            "View My Profile",
            "Edit My Profile",
            "Delete My Account",
            "Logout",
            "Exit Application"
        ]

        choice = display_menu(options)

        if choice == 1:  # Games
            show_games_menu()
        if choice == 2:  # View Profile
            display_user_profile(user=user)
            return True
        elif choice == 3:  # Edit Profile
            show_edit_profile_screen(current_user=user)
        elif choice == 4:  # Delete Account
            if not show_delete_account_screen():
                # Account was deleted, end session
                return False
        elif choice == 5:  # Logout
            user_controller.logout_user()
            return False
        elif choice == 6:  # Exit
            user_controller.logout_user()
            print("\nExiting application. Goodbye!")
            exit(0)
