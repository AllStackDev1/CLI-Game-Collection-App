import sqlite3
from db.connection import Database
from models.user import User


class UserRepository:
    """Repository for User database operations."""

    @staticmethod
    def save(user):
        """Save a User object to the database."""
        try:
            if UserRepository.email_exists(user.email):
                print("Error: This email is already registered.")
                return False
            with Database.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (user.name, user.email, user.password)
            ) as cursor:
                user.id = cursor.lastrowid  # Get the ID of the inserted row
            return True
        except sqlite3.IntegrityError:
            return False

    @staticmethod
    def find_by_id(user_id):
        """
        Find a user by ID
        
        Args:
            user_id (int): The ID of the user to find
            
        Returns:
            dict: User data if found, None otherwise
        """
        with Database.execute(
            "SELECT id, name, email, created_at FROM users WHERE id = ?", 
            (user_id,)
        ) as cursor:
            user_data = cursor.fetchone()

            if user_data:
                # Convert tuple to User object
                return User(
                    id=user_data[0],
                    name=user_data[1],
                    email=user_data[2],
                    password=None,
                    created_at=user_data[3],
                    password_is_hashed=True
                )
        return None

    @staticmethod
    def update(user_id, data):
        """
        Update an existing user record in the database
        
        Args:
            user_id (int): The ID of the user to update
            data (dict): Dictionary containing fields to update
                
        Returns:
            tuple: (success, message, user_data)
                success (bool): True if update succeeds, False otherwise
                message (str): Success/error message
                user_data (dict): Updated user data if successful, None otherwise
        """
        try:
            # Early return if no data
            if not data:
                return False, "No data provided for update", None
            
            # Check if the user exists
            existing_user = UserRepository.find_by_id(user_id)
            print(existing_user)
            if not existing_user:
                return False, f"User with ID {user_id} not found", None
                
            # Build update SQL parts
            update_parts = []
            params = []
            
            # Add fields to update (simple mapping only, no validation)
            valid_fields = ['name', 'email', 'password']
            for field in valid_fields:
                if field in data and data[field] is not None:
                    update_parts.append(f"{field} = ?")
                    params.append(data[field])
            
            # If no fields to update, return early
            if not update_parts:
                return False, "No valid fields to update", None
            
            # Build and execute the SQL query
            sql = f"UPDATE users SET {', '.join(update_parts)} WHERE id = ?"
            params.append(user_id)
            
            with Database.execute(sql, tuple(params)) as cursor:
                # Check if update was successful
                if cursor.rowcount == 0:
                    return False, "No changes made", None
                
                # Get the updated user data
                updated_user = UserRepository.find_by_id(user_id)
                return True, "User updated successfully", updated_user
            
        except Exception as e:
            return False, f"Database error: {str(e)}", None

    @staticmethod
    def delete(user_id):
        """
        Delete a user record from the database
        
        Args:
            user_id (int): The ID of the user to delete
            
        Returns:
            tuple: (success, message)
                success (bool): True if deletion succeeds, False otherwise
                message (str): Success/error message
        """
        try:
            # Check if user exists before attempting deletion
            existing_user = UserRepository.find_by_id(user_id)
            if not existing_user:
                return False, f"User with ID {user_id} not found"
            
            # Execute the deletion
            with Database.execute("DELETE FROM users WHERE id = ?", (user_id,)) as cursor:
            
                # Check if delete was successful
                if cursor.rowcount == 0:
                    return False, "No user was deleted"
                    
                return True, "User deleted successfully"
            
        except Exception as e:
            return False, f"Database error during deletion: {str(e)}"

    @staticmethod
    def find_by_email(email):
        """Retrieve a user by email."""
        with Database.execute(
            "SELECT id, name, email, password, created_at FROM users WHERE email = ?",
            (email.lower(),)
        ) as cursor:
            user_data = cursor.fetchone()

            if user_data:
                # Convert tuple to User object
                return User(
                    id=user_data[0],
                    name=user_data[1],
                    email=user_data[2],
                    password=user_data[3],
                    created_at=user_data[4],
                    password_is_hashed=True
                )
        return None

    @staticmethod
    def email_exists(email):
        """Check if an email already exists in the database."""
        with Database.execute(
            "SELECT COUNT(*) FROM users WHERE email = ?",
            (email.lower(),)
        ) as cursor:
            count = cursor.fetchone()[0]

        return count > 0