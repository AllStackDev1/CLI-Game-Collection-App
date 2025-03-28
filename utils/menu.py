


def display_menu(title, options):
    """
    Display a menu with numbered options.

    Args:
        title (str): The menu title
        options (list): List of option strings

    Returns:
        int: The selected option index (0-based)
    """
    console = Console()

    # Clear the screen for better presentation
    console.clear()

    print(f"\n=== {title} ===")

    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            if 1 <= choice <= len(options):
                return choice - 1  # Convert to 0-based index
            print(f"Please enter a number between 1 and {len(options)}")
        except ValueError:
            print("Please enter a valid number")