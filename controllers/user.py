import getpass
from rich.console import Console
from rich.panel import Panel
from prompt_toolkit import prompt

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


def update_user_details(user_data):
    """
    Update the current user's profile information
    
    Args:
        user_data (dict): The user data to update (name, email, password)
    
    Returns:
        tuple: (success, message)
            success (bool): True if update succeeds, False otherwise
            message (str): Success/error message
    """
    # Get the current user
    current_user = Session.get_current_user()
    if not current_user:
        return False, "No active user session found"
    
    # Create a clean dictionary with only valid fields
    update_data = {}
    
    # Validate name (if provided)
    if 'name' in user_data and user_data['name']:
        name = user_data['name'].strip()
        if len(name) < 2:
            return False, "Name must be at least 2 characters long"
        update_data['name'] = name
    
    # Validate email (if provided)
    if 'email' in user_data and user_data['email']:
        email = user_data['email'].strip()
        # Basic email validation
        if '@' not in email or '.' not in email or len(email) < 5:
            return False, "Please enter a valid email address"
        # Check if email is already in use by another user
        existing_user = UserRepository.find_by_email(email)
        if existing_user and existing_user['id'] != current_user['id']:
            return False, "Email address is already in use by another account"
        update_data['email'] = email
    
    # Handle password update (if provided)
    if 'password' in user_data and user_data['password']:
        password = user_data['password']
        # Password strength validation
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        # If confirmation password provided, check it matches
        if 'confirm_password' in user_data:
            if password != user_data['confirm_password']:
                return False, "Passwords do not match"
        
        # Hash the password before storing it
        hashed_password = PasswordHandler.hash_password(password)
        update_data['password'] = hashed_password
    
    # If there's nothing to update, return early
    if not update_data:
        return False, "No changes were made to your profile"
    
    # Call the repository to update the user
    success, message, updated_user = UserRepository.update(current_user['id'], update_data)
    
    # If update was successful, update the session
    if success and updated_user:
        # Update the session with new user details (excluding sensitive data)
        sensitive_fields = ['password']
        session_user = {k: v for k, v in updated_user.items() if k not in sensitive_fields}
        Session.set_current_user(session_user)
        
        return True, "Your profile has been updated successfully"
    
    # Return the result from the repository
    return success, message


def delete_current_user_account(confirm_password=None):
    """
    Delete the current user's account after confirmation
    
    Args:
        confirm_password (str, optional): Password confirmation for account deletion
        
    Returns:
        tuple: (success, message)
            success (bool): True if deletion succeeds, False otherwise
            message (str): Success/error message
    """
    # Get the current user
    current_user = Session.get_current_user()
    if not current_user:
        return False, "No active user session found"
    
    # If password confirmation is required and provided
    if confirm_password is not None:
        # Verify the password matches before proceeding
        is_valid = PasswordHandler.verify_password(confirm_password, current_user.get('password', ''))
        if not is_valid:
            return False, "Incorrect password. Account deletion cancelled."
    
    # Delete the user account
    success, message = UserRepository.delete(current_user['id'])
    
    # If deletion was successful, invalidate the session
    if success:
        Session.clear()
    
    return success, message


def logout_user():
    """Log out the current user."""
    user = Session.get_current_user()
    if user:
        print(f"\nGoodbye, {user.name}!")
        Session.logout()
    else:
        print("\nNo user is currently logged in")