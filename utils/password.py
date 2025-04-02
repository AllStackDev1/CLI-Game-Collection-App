import bcrypt


class PasswordHandler:
    """Handles secure password operations."""

    @staticmethod
    def hash_password(plain_password):
        """
        Hash a password using bcrypt.

        Args:
            plain_password: The plaintext password to hash

        Returns:
            str: The hashed password (includes the salt)
        """
        # Convert password to bytes if it's not already
        if isinstance(plain_password, str):
            password_bytes = plain_password.encode('utf-8')
        else:
            password_bytes = plain_password

        # Generate a salt and hash the password
        # Using 12 rounds (work factor) - good balance of security and performance
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)

        # Return the hash as a string
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Verify a password against its hash.

        Args:
            plain_password: The plaintext password to check
            hashed_password: The stored hash to check against

        Returns:
            bool: True if the password matches, False otherwise
        """
        # Convert inputs to bytes if they're not already
        if isinstance(plain_password, str):
            password_bytes = plain_password.encode('utf-8')
        else:
            password_bytes = plain_password

        if isinstance(hashed_password, str):
            hash_bytes = hashed_password.encode('utf-8')
        else:
            hash_bytes = hashed_password

        # Check if the password matches the hash
        try:
            return bcrypt.checkpw(password_bytes, hash_bytes)
        except Exception:
            # If there's any error, fail securely
            return False