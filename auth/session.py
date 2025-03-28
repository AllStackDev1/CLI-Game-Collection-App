class Session:
    """Manages user sessions."""

    _current_user = None

    @classmethod
    def login(cls, user):
        """Set the current logged-in user."""
        cls._current_user = user

    @classmethod
    def logout(cls):
        """Log out the current user."""
        cls._current_user = None

    @classmethod
    def get_current_user(cls):
        """Get the currently logged in user."""
        return cls._current_user

    @classmethod
    def is_authenticated(cls):
        """Check if a user is currently logged in."""
        return cls._current_user is not None
