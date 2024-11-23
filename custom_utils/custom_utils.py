import os
import random
import smtplib
from email.mime.text import MIMEText


class CustomException(Exception):
    """
    Custom exception class to handle application-specific errors.

    Attributes:
        message (str): The error message associated with the exception.
        status_code (int): The HTTP status code to return in case of an error.
    """

    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code


def send_email(email: str, subject: str, html_content: str):
    """
    Send email via SMTP using Gmail's SMTP server.

    Args:
        email (str): The recipient's email address.
        subject (str): The subject of the email.
        html_content (str): The content of the email in HTML format.

    Returns:
        dict: A dictionary containing the status and message of the email sending process.

    Raises:
        CustomException: If there are issues with SMTP authentication, recipient address,
                         or any other SMTP error.
    """
    sender_email = os.getenv("SENDER_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not sender_email or not smtp_password:
        raise CustomException(
            "Sender email or password is not set. Please check environment variables.",
            status_code=403)

    msg = MIMEText(html_content, 'html')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = email

    try:
        # Using Gmail's SMTP server with SSL on port 465
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, smtp_password)
            smtp_server.sendmail(sender_email, email, msg.as_string())
        return {"email": email}
    except smtplib.SMTPAuthenticationError as exc:
        raise CustomException(
            "Failed to authenticate with the SMTP server. Please check your email and password.",
            status_code=401) from exc
    except smtplib.SMTPRecipientsRefused as exc:
        raise CustomException(
            "Recipient address refused. Please check the recipient's email address.",
            status_code=400) from exc
    except smtplib.SMTPException as e:
        raise CustomException(
            f"SMTP error occurred: {str(e)}", status_code=500
        ) from e
    except Exception as e:
        raise CustomException(
            f"An unexpected error occurred: {str(e)}", status_code=500
        ) from e


def generate_otp():
    """
    Generate a 6-digit OTP (One-Time Password).

    Returns:
        int: A randomly generated 6-digit OTP.

    Raises:
        RuntimeError: If the generated OTP is out of the expected range.
    """
    try:
        print("generate otp")
        otp = random.randint(100000, 999999)
        if otp < 100000 or otp > 999999:
            raise RuntimeError(
                "Generated OTP is out of the expected range.")
        return otp
    except Exception as e:
        raise RuntimeError(
            f"An error occurred while generating OTP: {str(e)}"
        ) from e
