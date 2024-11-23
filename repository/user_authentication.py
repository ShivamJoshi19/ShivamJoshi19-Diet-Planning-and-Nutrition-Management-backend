from datetime import datetime, timezone
import uuid
from bson import ObjectId
from pymongo.errors import PyMongoError
from custom_utils import custom_utils
from connections.mongo_connection import MongoConnection
from models.user_authentication import UserModel

db = MongoConnection.get_db()


class UserRepository:

    @staticmethod
    def get_user_by_email(collection_name, email: str):
        """
        Fetches a user document from MongoDB based on email.

        Args:
            email (str): User's email.

        Returns:
            dict: User document if found, otherwise None.
        """
        collection = db[collection_name]
        return collection.find_one({"email": email})

    @staticmethod
    def register_or_update_user(collection_name: str, user_id: str, email: str,
                                otp: str, hashed_password: str):
        """
        Registers a new user or updates an inactive user's record.

        Args:
            collection_name (str): The name of the MongoDB collection.
            email (str): User's email.
            otp (str): One-Time Password.
            hashed_password (str): Hashed password.

        Returns:
            str: Inserted or updated user ID.

        Raises:
            custom_utils.CustomException: If the user is already registered with is_active=True.
        """
        try:
            collection = db[collection_name]

            # Check if the email already exists
            existing_user = collection.find_one({"email": email})

            if existing_user:
                if existing_user.get("is_active", False):
                    # Raise error if the user is already registered and active
                    raise custom_utils.CustomException(
                        "User is already registered.", status_code=400)

                # Update the inactive user record
                user_id = existing_user["user_id"]
                update_data = {
                    "email": email,
                    "password": hashed_password,
                    "otp": otp,
                    "otp_created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc),
                    "is_active": False,
                }
                result = collection.update_one(
                    {"user_id": user_id}, {"$set": update_data})
                return user_id
            else:
                user_data = {
                    "user_id": user_id,
                    "email": email,
                    "password": hashed_password,
                    "otp": otp,
                    "otp_created_at": datetime.now(timezone.utc),
                    "user_role": "user",
                    "first_name": None,
                    "last_name": None,
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc),
                    "is_active": False,
                }
                result = collection.insert_one(user_data)
                return user_id

        except custom_utils.CustomException as e:
            raise e
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while registering or updating the user: {str(e)}")
