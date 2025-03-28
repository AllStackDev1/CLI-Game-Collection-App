import getpass
from rich.console import Console
from rich.panel import Panel
from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

from models.user import User, ValidationError
from repositories.user import UserRepository
from auth.password import PasswordHandler
from auth.session import Session


def register_user():
    """Register a new user with interactive validation using the repository pattern."""
    print("\n=== User Registration ===")

    # Interactive registration with validation
    while True:
        try:
            # Name validation - keep asking until valid
            try:
                name = input("Enter your name: ")
                user = User("temp", "temp@example.com", "Password123!")
                user.name = name  # This will validate
            except ValidationError as e:
                print(f"Invalid name: {str(e)}")
                continue

            # Email validation - keep asking until valid
            try:
                email = input("Enter your email: ")
                user.email = email  # This will validate

                # Check if email already exists
                if UserRepository.email_exists(email):
                    print("Error: This email is already registered.")
                    continue
            except ValidationError as e:
                print(f"Invalid email: {str(e)}")
                continue

            # Password validation with masking - keep asking until valid
            valid_password = False
            while not valid_password:
                try:
                    password = getpass.getpass("Enter your password: ")
                    password_confirm = getpass.getpass("Confirm your password: ")

                    if password != password_confirm:
                        print("Error: Passwords don't match.")
                        continue

                    user.password = password  # This will validate
                    valid_password = True
                except ValidationError as e:
                    print(f"Invalid password: {str(e)}")

            # If we get here, all validation passed - create the user
            user = User(name=name, email=email, password=password)

            # Save user via repository
            if UserRepository.save(user):
                # Set the user in the session
                Session.login(user)
                print(f"\nRegistration successful, welcome to the Archive, {user.name}!")
                return user
            else:
                print("Error: Failed to register user.")
                return None

        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None


def login_user():
    """
    Log in a user with email and password.

    Returns:
        User: The logged-in user if successful, None otherwise
    """
    console = Console()

    console.print(Panel("Login to your account"))

    # Get user credentials
    email = prompt("Email: ")
    password = prompt("Password: ", is_password=True)
    # password = getpass.getpass("Password: ")

    # Find the user by email
    user = UserRepository.find_by_email(email)

    if not user:
        console.print(f"[red]Invalid email or password[/red]")
        return False

    # Verify password
    if not PasswordHandler.verify_password(password, user.password):
        console.print(f"[red]Invalid email or password[/red]")
        return False

    # Set the user in the session
    Session.login(user)

    print(f"\nWelcome back, {user.name}!")
    return user


def display_user_profile(user=None):
    """Display user profile information."""
    # Get current user if none provided
    if user is None:
        user = Session.get_current_user()
        if not user:
            print("No user is logged in")
            return

    print("\n=== User Profile ===")
    print(f"ID: {user.id}")
    print(f"Name: {user.name}")
    print(f"Email: {user.email}")
    print(f"Account Created: {user.created_at}")

    # update functionality
    # delete account 
    # forgot password

    input("\nPress Enter to continue...")


def logout_user():
    """Log out the current user."""
    user = Session.get_current_user()
    if user:
        print(f"\nGoodbye, {user.name}!")
        Session.logout()
    else:
        print("\nNo user is currently logged in")