from fastapi import FastAPI, APIRouter, status
from services.user_profile import UserProfileService
from dto.request_dto.user_authentication_request_dto import (
UserProfileDto,UserGetProfileDto)
from dto.response_dto.response_dto import ResponseDto
from custom_utils import custom_utils

router = APIRouter()
app = FastAPI()


@router.post("/user-profile/", response_model=ResponseDto)
async def UserProfile(request: UserProfileDto):
    print("178")
    try:
        print("12")
        data = UserProfileService.profile_user(request.user_id, request.first_name,
                                         request.last_name, request.age, request.weight,
                                         request.height, request.gender)
        response = ResponseDto(
            Data={
                "user_id": data["user_id"],
                "first_name": data["first_name"],
                "last_name": data["last_name"],
                "age": data["age"],
                "weight": data["weight"],
                "height": data["height"],
                "gender": data["gender"],
                "is_active": data["is_active"], 
            },
            Success=True,
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

@router.post("/get-user-profile/", response_model=ResponseDto)
async def login(request: UserGetProfileDto):
    try:
        data = UserProfileService.get_user_profile(request.user_id)
        response = ResponseDto(
            Data={
                "user_id": data.get("user_id"),
                "first_name": data.get("first_name"),
                "age": data.get("age"),
                "weight": data.get("weight"),
                "height": data.get("height"),
                "gender": data.get("gender"),
                "is_active": data.get("is_active"),
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