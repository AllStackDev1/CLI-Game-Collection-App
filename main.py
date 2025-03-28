from db.connection import Database
from db.migration import MigrationManager
from auth.session import Session
from app.menu import display_welcome, show_auth_menu, show_main_menu


def main():
    """Main application entry point."""
    # Initialize database and apply migrations
    Database.initialize()
    print("Initializing database...")
    MigrationManager.migrate()

    # Show welcome message
    display_welcome()

    # Authentication loop
    while True:
        while not Session.is_authenticated():
            try:
                user = show_auth_menu()
                if user is None:
                    # User selected Exit
                    print("\nExiting application. Goodbye!")
                    return
            except KeyboardInterrupt:
                print("\nOperation cancelled by user. Exiting...")
                exit(0)

        # Main application menu
        continue_menu = show_main_menu()
        if not continue_menu:
            # User has logged out, break from this loop to return to login screen
            break

        print("\nThank you for using Archive!")


if __name__ == "__main__":
    main()
