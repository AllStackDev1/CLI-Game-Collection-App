def validate_input(prompt, validator_func, error_message):
    """
    Get and validate user input.

    Args:
        prompt (str): The input prompt to display
        validator_func (function): Function that returns True for valid input
        error_message (str): Message to display on validation failure

    Returns:
        str: Validated user input
    """
    while True:
        user_input = input(prompt)
        try:
            if validator_func(user_input):
                return user_input
            else:
                print(f"Error: {error_message}")
        except Exception as e:
            print(f"Error: {str(e)}")