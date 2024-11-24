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
                                otp: int, hashed_password: str):
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
                    "is_profile_set": False,
                    "is_active": False,
                }
                collection.update_one(
                    {"user_id": user_id}, {"$set": update_data})
                return user_id
            else:
                now = datetime.now(timezone.utc)
                user_data = UserModel(
                    user_id=user_id,
                    email=email,
                    password=hashed_password,
                    otp=otp,
                    otp_created_at=now,
                    user_role="user",
                    created_at=now,
                    updated_at=now,
                    is_profile_set=False,
                    is_active=False
                )
                collection.insert_one(user_data.dict())
                return user_id

        except custom_utils.CustomException as e:
            raise e
        except Exception as e:
            raise RuntimeError(
                f"An error occurred while registering or updating the user: {str(e)}")

    @staticmethod
    def update_user_by_email(collection_name, email: str, update_data: dict):
        """
        Updates the user document based on the email.

        Args:
            email (str): The email of the user to update.
            update_data (dict): The fields to update in the user document.

        Raises:
            custom_utils.CustomException: If an error occurs while updating the user.
        """
        collection = db[collection_name]
        result = collection.update_one(
            {"email": email}, {"$set": update_data})
        if result.matched_count == 0:
            raise custom_utils.CustomException(
                "Failed to update user.", status_code=500)

    @staticmethod
    def update_user_by_id(user_id: str, update_data: dict, collection_name):
        """
        Updates a user's document in the database by user ID.

        Args:
            user_id (str): The user's ID.
            update_data (dict): A dictionary of fields to update.

        Raises:
            Exception: If there is an issue updating the user document.
        """
        try:
            collection = db[collection_name]
            result = collection.update_one(
                {"user_id": user_id},  # Match the user by ID
                {"$set": update_data}  # Set the fields to update
            )
            if result.matched_count == 0:
                raise custom_utils.CustomException(
                    message=f"User with ID {user_id} not found.",
                    status_code=404
                )
            if result.modified_count == 0:
                raise custom_utils.CustomException(
                    message="No changes were made to the user document.",
                    status_code=400
                )
        except Exception as e:
            raise Exception(f"Failed to update user: {e}") from e

    @staticmethod
    def update_user_status(user_id: str, access_token: str, collection_name):
        """
        Updates the user's access token in the database.

        Args:
            user_id (str): The user's ID.
            access_token (str): The new JWT access token.

        Raises:
            Exception: If there is an issue updating the user's access token.
        """
        try:
            update_data = {"access_token": access_token,
                           "updated_at": datetime.now(timezone.utc)}
            UserRepository.update_user_by_id(
                user_id, update_data, collection_name)
        except Exception as e:
            raise Exception(f"Failed to update access token: {e}") from e
