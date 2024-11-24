from pydantic import BaseModel, Field, field_validator, EmailStr


class UserLoginRegisterDto(BaseModel):
    email: EmailStr
    password: str


class VerifyOTPRequest(BaseModel):
    email: str
    otp: int


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: int
    new_password: str


class UserProfileDto(BaseModel):
    user_id: str = Field(...,)
    first_name: str = Field(...,
                            description="The user's first name")
    last_name: str = Field(...,
                           description="The user's last name")
    age: str = Field(...,
                     description="The user's age")
    weight: str = Field(..., description="")
    height: str = Field(...,
                        description="")
    gender: str = Field(...,
                        description="")


class UserGetProfileDto(BaseModel):
    user_id: str = Field(...,)
