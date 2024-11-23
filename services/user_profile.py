import uuid
from repository.profile_setup import UserProfileRepository
from custom_utils import custom_utils
from fastapi import HTTPException

USER_COLLECTION = "UserProfile"


class UserProfileService:

    @staticmethod
    def profile_user(user_id: str, first_name: str, last_name:str, age: int, weight:str, height:str, gender: str):
        """
        Registers a new user with the given email and password. If the user already exists,
        it checks if the user is inactive and reuses the user ID. Otherwise, a new user ID
        is generated. The OTP for email verification is sent to the user's email address.

        Args:
            email (str): The user's email address.
            password (str): The user's plain-text password.

        Raises:
            custom_utils.CustomException: If the user is already registered or email sending
            fails.
            HTTPException: If there is a ClientError during registration.

        Returns:
            dict: A response with the email and success message.
        """
        try:
            user_id = UserProfileRepository.profile_set_up(
                USER_COLLECTION, user_id, first_name, last_name, age , weight, height, gender)
            return {
                "message": "Profile Setup Successfully"
            }
        except Exception as e:
            raise e

