from fastapi import FastAPI, APIRouter, status
from services import user_profile
from dto.request_dto import user_authentication_request_dto, user_query_request_dto
from dto.response_dto.response_dto import ResponseDto
from custom_utils import custom_utils

router = APIRouter()
app = FastAPI()


@router.post("/profile/", response_model=ResponseDto)
async def UserProfile(request: user_authentication_request_dto.UserProfileDto):
    try:
        data = user_profile.UserProfileService.profile_user(request.user_id, request.first_name,
                                                            request.last_name, request.age, request.weight,
                                                            request.height, request.gender)
        response = ResponseDto(
            Data={
                "user_id": data.get("user_id")
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


@ router.post("/get-profile/", response_model=ResponseDto)
async def login(request: user_authentication_request_dto.UserGetProfileDto):
    try:
        data = user_profile.UserProfileService.get_user_profile(
            request.user_id)
        response = ResponseDto(
            Data={
                "user_id": data.get("user_id"),
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "email": data.get("email"),
                "access_token": data.get("access_token"),
                "user_role": data.get("user_role"),
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


@router.post("/send-query/", response_model=ResponseDto)
async def send_user_query(request: user_query_request_dto.UserQueryRequestDto):
    try:
        data = user_profile.UserProfileService.send_user_query(
            request.user_id, request.allergic_to_food,
            request.preference, request.disease, request.diet_plan, request.query_message)
        response = ResponseDto(
            Data={
                "dietitian_email": data["dietitian_email"],
                "user_email": data["user_email"],
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
