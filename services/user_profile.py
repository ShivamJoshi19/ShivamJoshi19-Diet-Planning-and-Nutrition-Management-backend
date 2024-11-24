from datetime import datetime, timezone
import os
from models.user_query import UserQueryModel
from repository.profile_setup import UserProfileRepository
from repository.user_authentication import UserRepository
from custom_utils import custom_utils

USER_PROFILE_COLLECTION = "UserProfile"
USER_COLLECTION = "User"
USER_QUERY_COLLECTION = "UserQuery"


class UserProfileService:

    @staticmethod
    def profile_user(user_id: str, first_name: str, last_name: str, age: str,
                     weight: str, height: str, gender: str):
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
            user_document = UserProfileRepository.get_user_by_user_id(
                USER_PROFILE_COLLECTION, user_id)
            if user_document:
                raise custom_utils.CustomException(
                    "Profile already exists for the user.", status_code=409)
            user_id = UserProfileRepository.profile_set_up(
                USER_PROFILE_COLLECTION, user_id, first_name, last_name, age,
                weight, height, gender)
            update_data = {"is_profile_set": True,
                           "updated_at": datetime.now(timezone.utc)}
            UserRepository.update_user_by_id(
                user_id, update_data, USER_COLLECTION)
            return {
                "user_id": user_id,
                "message": "Profile Setup Successfully"
            }
        except Exception as e:
            raise e

    @staticmethod
    def get_user_profile(user_id: str) -> dict:

        try:
            user_document = UserProfileRepository.get_user_by_user_id(
                USER_PROFILE_COLLECTION, user_id)
            user_data = user_document

            user_id = user_data.get('user_id')
            user_doc = UserProfileRepository.get_user_email_by_id(
                USER_COLLECTION, user_id)
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')
            email = user_doc.get('email')
            access_token = user_doc.get('access_token')
            user_role = user_doc.get('user_role')
            age = user_data.get('age')
            weight = user_data.get('weight')
            height = user_data.get('height')
            gender = user_data.get('gender')
            is_active = user_data.get('is_active')
            # Return Profile response
            return {
                "message": "Data fetch successful",
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "access_token": access_token,
                "user_role": user_role,
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

    @staticmethod
    def send_user_query(user_id, allergic_to_food, preference,
                        disease, diet_plan, query_message):
        try:
            user_document = UserProfileRepository.get_user_by_user_id(
                USER_PROFILE_COLLECTION, user_id)
            if not user_document:
                raise custom_utils.CustomException(
                    message="User not found", status_code=404)
            user_data = user_document
            user_doc = UserProfileRepository.get_user_email_by_id(
                USER_COLLECTION, user_id)
            user_email = user_doc.get('email')
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')
            full_name = f"{first_name} {last_name}"
            query = UserQueryModel(
                user_id=user_id,
                first_name=first_name,
                allergic_to_food=allergic_to_food,
                preference=preference,
                disease=disease,
                diet_plan=diet_plan,
                query_message=query_message,
                status="pending",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
                is_active=True
            )
            UserProfileRepository.create_query(USER_QUERY_COLLECTION, query)
            subject = "HealthQuest Query Submission"
            html_content_for_user_query = custom_utils.render_template("user_query_submission.html", {
                "full_name": full_name
            })
            email_response = custom_utils.send_email(
                user_email, subject, html_content_for_user_query)
            return {
                "dietitian_email": os.getenv("DIETITIAN_EMIAL"),
                "user_email": email_response['email'],
                "user_id": user_id,
                "first_name": first_name,
                "message": "Query submitted successfully!"
            }
        except Exception as e:
            raise e

    @staticmethod
    def get_query_status(user_id: str):
        try:
            user_query = UserProfileRepository.get_user_by_user_id(USER_QUERY_COLLECTION,
                                                                   user_id)
            query_status = user_query.get('status')
            return {
                "query_status": query_status,
                "message": "User Query Status Retrieved Successfully"
            }
        except Exception as e:
            raise e
