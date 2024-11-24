from typing import Optional
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from hashlib import sha256
from repository.user_authentication import UserRepository
from custom_utils import custom_utils, jwt
from fastapi import HTTPException

USER_COLLECTION = "User"


class UserService:

    @staticmethod
    def register_user(email: str, password: str):
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
            password = UserService.hash_password(password)
            otp = custom_utils.generate_otp()
            user_id = str(uuid.uuid4())
            user_id = UserRepository.register_or_update_user(
                USER_COLLECTION, user_id, email, otp, password)
            subject = "Nutrionist Verification OTP"
            html_content = f"""<html><body><p>Your OTP is: {
                otp}</p></body></html>"""
            email_response = custom_utils.send_email(
                email, subject, html_content)
            if not email_response or "email" not in email_response:
                raise custom_utils.CustomException("Failed to send email.",
                                                   status_code=500)
            return {
                "email": email_response["email"],
                "user_id": user_id,
                "message": "User registered successfully. OTP sent via email."
            }
        except Exception as e:
            raise e

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes the user's password using the SHA-256 algorithm.

        Args:
            password (str): The user's plain-text password.

        Returns:
            str: The hashed password.

        Raises:
            Exception: If an error occurs during hashing.
        """
        try:
            hash_password = sha256(password.encode('utf-8')).hexdigest()
            return hash_password
        except Exception as e:
            raise e

    @staticmethod
    def verify_otp(email: str, otp: int) -> dict:
        """
        Verifies the OTP for the user associated with the provided email. The OTP is
        checked for correctness and expiration (within 5 minutes).

        Args:
            email (str): The user's email address.
            otp (int): The OTP to verify.

        Raises:
            custom_utils.CustomException: If the OTP is invalid, expired, or if any
            other issue occurs.

        Returns:
            dict: The user ID, email, and success message after OTP verification.
        """
        try:
            # Fetch the user document by email
            user_document = UserRepository.get_user_by_email(
                USER_COLLECTION, email)
            if not user_document:
                raise custom_utils.CustomException(
                    "User not found", status_code=404)
            user_data = user_document
            stored_otp = user_data.get("otp")
            if stored_otp != otp:
                raise custom_utils.CustomException(
                    "Invalid OTP", status_code=400)
            otp_created_at = user_data.get("otp_created_at")
            if not otp_created_at:
                raise custom_utils.CustomException(
                    "OTP creation time not found", status_code=400)
            if isinstance(otp_created_at, str):
                otp_created_at = datetime.fromisoformat(otp_created_at)
            if otp_created_at.tzinfo is None:
                otp_created_at = otp_created_at.replace(tzinfo=timezone.utc)

            # Check OTP expiration (within 5 minutes)
            if (datetime.now(timezone.utc) - otp_created_at).seconds > 300:
                raise custom_utils.CustomException(
                    "OTP expired", status_code=400)

            # Update user fields in MongoDB: otp, is_active, and updated_at
            update_data = {
                "otp": otp,  # Clear OTP after successful verification
                "is_active": True,
                "updated_at": datetime.now(timezone.utc),
            }
            UserRepository.update_user_by_email(
                USER_COLLECTION, email, update_data)

            return {
                "user_id": user_data.get("user_id"),
                "email": email,
                "message": "OTP verified successfully."
            }

        except ValueError as ve:
            raise custom_utils.CustomException(
                f"Invalid value encountered: {str(ve)}", status_code=500
            )
        except Exception as e:
            raise e

    def login_user(email: str, password: str) -> dict:
        """
        Authenticates a user by checking their email and password. If the login is
        successful, a JWT access token is generated and user details are returned.

        Args:
            email (str): The user's email address.
            password (str): The user's plain-text password.

        Raises:
            custom_utils.CustomException: If the email or password is invalid or not found.

        Returns:
            dict: A response containing the user ID, access token, user role, and success message.
        """
        try:
            user_document = UserRepository.get_user_by_email(
                USER_COLLECTION, email)
            if not user_document:
                raise custom_utils.CustomException(
                    "User not found", status_code=404)
            user_data = user_document
            # Validate password
            stored_password = user_data.get('password')
            if not stored_password:
                raise custom_utils.CustomException(
                    status_code=500, message="Password not found for the user.")
            if UserService.hash_password(password) != stored_password:
                raise custom_utils.CustomException(
                    status_code=401, message="Invalid password")

            # Extract user details
            user_id = user_data.get('user_id')
            user_role = user_data.get('user_role')
            is_profile_set = user_data.get('is_profile_set')
            is_active = user_data.get('is_active')

            # Generate a new JWT token
            access_token = jwt.create_access_token(data={"id": user_id})

            # Update user access token in the database
            UserRepository.update_user_status(
                user_id, access_token, USER_COLLECTION)

            # Return login response
            return {
                "message": "Login Successful",
                "user_id": user_id,
                "access_token": access_token,
                "user_role": user_role,
                "is_profile_set": is_profile_set,
                "is_active": is_active
            }
        except KeyError as ke:
            raise custom_utils.CustomException(
                f"Missing key in user data: {str(ke)}", status_code=500)
        except Exception as e:
            raise e

    @staticmethod
    def forget_password(email: str):
        try:
            user_document = UserRepository.get_user_by_email(
                USER_COLLECTION, email)
            if not user_document:
                raise custom_utils.CustomException(
                    "User not found", status_code=404)
            user_data = user_document
            user_id = user_data.get('user_id')
            otp = custom_utils.generate_otp()
            update_data = {
                "otp": otp,
                "otp_created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc)
            }
            UserRepository.update_user_by_id(
                user_id, update_data, USER_COLLECTION)
            subject = "Nutrionist Verification OTP"
            html_content = f"<html><body><p>Your OTP is: {otp}</p></body></html>"
            email_response = custom_utils.send_email(
                email, subject, html_content)
            return {"email": email_response["email"],
                    "message": "OTP sent via email."}
        except Exception as e:
            raise e

    @staticmethod
    def reset_password(email: str, otp: int, new_password: str):
        try:
            user_document = UserRepository.get_user_by_email(
                USER_COLLECTION, email)
            if not user_document:
                raise custom_utils.CustomException(
                    "User not found", status_code=404)
            user_data = user_document
            user_id = user_data.get('user_id')
            stored_otp = user_data.get("otp")
            if stored_otp != otp:
                raise custom_utils.CustomException(
                    "Invalid OTP", status_code=400)
            otp_created_at = user_data.get("otp_created_at")
            if not otp_created_at:
                raise custom_utils.CustomException(
                    "OTP creation time not found", status_code=400)
            if isinstance(otp_created_at, str):
                otp_created_at = datetime.fromisoformat(otp_created_at)
            if otp_created_at.tzinfo is None:
                otp_created_at = otp_created_at.replace(tzinfo=timezone.utc)
            if (datetime.now(timezone.utc) - otp_created_at).seconds > 300:
                raise custom_utils.CustomException(
                    "OTP expired", status_code=400)
            password = UserService.hash_password(new_password)
            update_data = {
                "password": password,
                "updated_at": datetime.now(timezone.utc)
            }
            UserRepository.update_user_by_id(
                user_id, update_data, USER_COLLECTION)
            return {"email": email,
                    "message": "Password reset successfully."}
        except Exception as e:
            raise e
