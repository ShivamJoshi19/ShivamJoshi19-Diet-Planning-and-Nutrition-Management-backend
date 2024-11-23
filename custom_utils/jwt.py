import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import toml
import jwt
from custom_utils import custom_utils

load_dotenv()
config_path = os.path.abspath("config.toml")
config = toml.load(config_path)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config['JWT']["ACCESS_TOKEN_EXPIRE_MINUTES"]


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JSON Web Token (JWT) access token.

    Args:
        data (dict): The payload data to include in the token.
        expires_delta (timedelta, optional): The duration for which the token is valid. 
        If not provided, a default expiration time will be used.

    Returns:
        str: The encoded JWT access token.

    Raises:
        ValueError: If the data is empty or not a valid dictionary.
        Exception: If there is an error during JWT encoding.
    """
    if not isinstance(data, dict) or not data:
        raise ValueError("Data must be a non-empty dictionary.")
    to_encode = data.copy()
    try:
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + \
                timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        raise Exception(f"Error encoding JWT: {e}") from e


def decode_access_token(token: str) -> dict:
    """
    Decode a JSON Web Token (JWT) access token and return the payload.

    Args:
        token (str): The JWT access token to decode.

    Returns:
        dict: The decoded payload of the JWT.

    Raises:
        CustomException: If the token is expired or invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError as jwtexp:
        raise custom_utils.CustomException(status_code=401,
                                           message="Token has expired") from jwtexp
    except jwt.PyJWTError as jwterr:
        raise custom_utils.CustomException(status_code=403,
                                           message="Invalid token") from jwterr
