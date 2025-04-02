import re
from datetime import datetime
from utils.password import PasswordHandler


class ValidationError(Exception):
    """Exception raised for validation errors in the model."""
    pass


class User:
    """User model with validation."""
    def __init__(self, name, email, password, id=None, created_at=None, password_is_hashed=False):
        self.id = id
        self._name = None
        self._email = None
        self._password = None
        self._created_at = created_at or datetime.now()
        self._password_is_hashed = password_is_hashed

        # Set properties with validation
        self.name = name
        self.email = email

        # Handle password differently based on whether it's already hashed
        if password_is_hashed:
            self._password = password  # Already hashed, store directly
        else:
            self.password = password  # Not hashed, validate and hash

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Validate name
        if not value or len(value.strip()) < 3:
            raise ValidationError("Name must be at least 3 characters long.")
        self._name = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not value or not re.match(email_pattern, value):
            raise ValidationError("Invalid email format.")
        self._email = value.lower()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        """Validate and hash the password."""
        # Skip validation if the password is already hashed
        if self._password_is_hashed:
            self._password = value
            return

        # Validate password strength
        if not value or len(value) < 6:
            raise ValidationError("Password must be at least 6 characters long")
        # if not any(char.isdigit() for char in value):
        #     raise ValidationError("Password must contain at least one number")
        # if not any(char.isupper() for char in value):
        #     raise ValidationError("Password must contain at least one uppercase letter")

        # Hash the password
        self._password = PasswordHandler.hash_password(value)
        self._password_is_hashed = True

    @property
    def created_at(self):
        return self._created_at

    def to_dict(self):
        """Convert User object to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,  # Note: In a real app, you'd never return this
            'created_at': self.created_at
        }

    @classmethod
    def from_db_row(cls, row):
        """Create a User object from a database row."""
        return cls(
            id=row[0],
            name=row[1],
            email=row[2],
            password=row[3],
            created_at=row[4],
            password_is_hashed=True  # Password from DB is already hashed
        )