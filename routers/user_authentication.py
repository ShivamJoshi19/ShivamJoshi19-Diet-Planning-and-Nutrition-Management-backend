from fastapi import FastAPI, APIRouter, status
from services.user_authentication import UserService
from dto.request_dto.user_authentication_request_dto import (
    UserLoginRegisterDto, VerifyOTPRequest, ResetPasswordRequest,
    ForgotPasswordRequest)
from dto.response_dto.response_dto import ResponseDto
from custom_utils import custom_utils

router = APIRouter()
app = FastAPI()


@router.post("/registration/", response_model=ResponseDto)
async def register(request: UserLoginRegisterDto):
    try:
        data = UserService.register_user(request.email, request.password)
        response = ResponseDto(
            Data={
                "email": data["email"],
                "user_id": data["user_id"]
            },
            Success=True,
            Message=data["message"],
            Status=status.HTTP_200_OK,
        )
    except custom_utils.CustomException as e:
        response = ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=e.status_code
        )
    except Exception as e:
        response = ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response


@router.post("/verify-otp/", response_model=ResponseDto)
async def verify_otp(request: VerifyOTPRequest):
    """
    Verifies the OTP provided by the user.

    Args:
        request (VerifyOTPRequest): The OTP verification request containing the
        user identifier and OTP.

    Returns:
        ResponseDto: The response indicating success or failure of the
        OTP verification.
    """
    try:
        data = UserService.verify_otp(email=request.email, otp=request.otp)
        response = ResponseDto(
            Data={
                "user_id": data.get("user_id"),
                "email": data.get("email"),
            },
            Success=True,
            Message=data["message"],
            Status=status.HTTP_200_OK
        )
    except custom_utils.CustomException as e:
        response = ResponseDto(
            Data={
                "is_active": False
            },
            Success=False,
            Message=str(e),
            Status=e.status_code
        )
    except Exception as e:
        response = ResponseDto(
            Data={
                "is_active": False
            },
            Success=False,
            Message=str(e),
            Status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response


@router.post("/login/", response_model=ResponseDto)
async def login(request: UserLoginRegisterDto):
    try:
        data = UserService.login_user(request.email, request.password)
        response = ResponseDto(
            Data={
                "user_id": data.get("user_id"),
                "access_token": data.get("access_token"),
                "is_active": data.get("is_active")
            },
            Success=True,
            Message=data["message"],
            Status=status.HTTP_200_OK,
        )
    except custom_utils.CustomException as e:
        response = ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=e.status_code
        )
    except Exception as e:
        response = ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response


@router.post("/password-forget/", response_model=ResponseDto)
async def forget_password(
        request: ForgotPasswordRequest):
    try:
        data = UserService.forget_password(request.email)
        response = ResponseDto(
            Data={"email": data["email"]},
            Success=True,
            Message=data["message"],
            Status=status.HTTP_200_OK,
        )
    except custom_utils.CustomException as e:
        response = ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=e.status_code
        )
    except Exception as e:
        response = ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response


@router.post("/password-reset/", response_model=ResponseDto)
async def reset_password(request: ResetPasswordRequest):
    try:
        data = UserService.reset_password(
            request.email, request.otp, request.new_password)
        response = ResponseDto(
            Data={"email": data["email"]},
            Success=True,
            Message=data["message"],
            Status=status.HTTP_200_OK,
        )
    except custom_utils.CustomException as e:
        response = ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=e.status_code
        )
    except Exception as e:
        response = ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response
