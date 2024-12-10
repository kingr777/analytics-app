import bcrypt
from config.database import get_database
from bson import Binary

class User:
    def __init__(self):
        try:
            self.db = get_database()
            self.users = self.db.users
            self.data = self.db.user_data
            
            # Create indexes for better performance
            self.users.create_index("username", unique=True)
            self.users.create_index("email", unique=True)
        except Exception as e:
            print(f"Error initializing User model: {e}")
            raise

    def create_user(self, username, password, email):
        try:
            # Input validation
            if not username or not password or not email:
                return False, "All fields are required"
            
            # Check if user exists
            if self.users.find_one({"$or": [
                {"username": username},
                {"email": email}
            ]}):
                return False, "Username or email already exists"
            
            # Hash password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            user = {
                "username": username,
                "password": Binary(hashed_password),  # Store as Binary
                "email": email
            }
            
            self.users.insert_one(user)
            return True, "User created successfully"
            
        except Exception as e:
            print(f"Error creating user: {e}")
            return False, "Error creating user"

    def verify_user(self, username, password):
        try:
            if not username or not password:
                return False, None
                
            user = self.users.find_one({"username": username})
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                # Remove password from user data before returning
                user.pop('password', None)
                return True, user
            return False, None
            
        except Exception as e:
            print(f"Error verifying user: {e}")
            return False, None

    def save_user_data(self, username, data_name, data):
        try:
            if not username or not data_name or data is None:
                return False
                
            # Update existing data or insert new
            result = self.data.update_one(
                {"username": username, "data_name": data_name},
                {"$set": {"data": data}},
                upsert=True
            )
            return result.acknowledged
            
        except Exception as e:
            print(f"Error saving user data: {e}")
            return False

    def get_user_data(self, username):
        try:
            if not username:
                return []
                
            return list(self.data.find(
                {"username": username},
                {"_id": 0, "password": 0}  # Exclude sensitive fields
            ))
            
        except Exception as e:
            print(f"Error retrieving user data: {e}")
            return []