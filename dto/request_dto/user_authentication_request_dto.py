from pydantic import BaseModel, Field, field_validator, EmailStr


class UserLoginRegisterDto(BaseModel):
    email: EmailStr
    password: str


class UserProfileDto(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50,
                            description="The user's first name")
    last_name: str = Field(..., min_length=1, max_length=50,
                           description="The user's last name")
    country: str = Field(..., min_length=1, max_length=50,
                         description="The user's country")
    gender: str = Field(..., description="The user's gender")
    user_role: str = Field(..., min_length=1, max_length=50,
                           description="The user's role")

    # Optional: Add a validator to ensure gender is a valid option
    @field_validator('gender')
    def validate_gender(cls, value):
        valid_genders = {"Male", "Female", "Other", "Prefer not to say"}
        if value not in valid_genders:
            raise ValueError(f"Gender must be one of {valid_genders}")
        return value


class VerifyOTPRequest(BaseModel):
    email: str
    otp: int


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: int
    new_password: str
