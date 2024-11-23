from typing import Optional
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from hashlib import sha256
from repository.user_authentication import UserRepository
from custom_utils import custom_utils
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
            print("otp", otp)
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
