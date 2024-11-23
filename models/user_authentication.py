from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, timezone


class UserModel(BaseModel):
    user_id: str = Field(...)
    user_role: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    access_token: Optional[str] = Field(None)
    otp: Optional[int] = Field(
        None, description="One-time password for authentication")
    otp_created_at: Optional[datetime] = Field(
        None, description="Timestamp when the OTP was created")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=False)


class UserProfileModel(BaseModel):
    user_id: str = Field(...)
    first_name: Optional[str] = Field(
        None, description="First name of the user")
    last_name: Optional[str] = Field(None, description="Last name of the user")
    age: int = Field(...)
    weight: float = Field(...)
    height: float = Field(...)
    gender: float = Field(...)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)
