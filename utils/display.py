import os
import platform


def clear_screen():
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def display_welcome():
    """Display welcome message."""
    clear_screen()
    print("=" * 40)
    print("      Welcome to the Archive App      ")
    print("=" * 40)
    print("\nYour ultimate CLI game collection")
