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

    @staticmethod
    def get_user_profile(user_id: str) -> dict:

        try:
            user_document= UserProfileRepository.get_user_by_user_id(
                USER_COLLECTION,user_id)
            user_data = user_document
            
            user_id = user_data.get('user_id')
            first_name = user_data.get('first_name')
            age = user_data.get('age'),
            weight = user_data.get('weight'),
            height = user_data.get('height'),
            gender = user_data.get('gender'),
            is_active= user_data.get('is_active')
            # Return Profile response
            return {
                "message": "Data fetch successful",
                "user_id": user_id,
                "first_name": first_name,
                "age": age,
                "weight": weight,
                "height": height,
                "gender": gender,
                "is_active": is_active
            }
        except KeyError as ke:
            raise custom_utils.CustomException(
                f"Missing key in user data: {str(ke)}", status_code=500)
        except Exception as e:
            raise e