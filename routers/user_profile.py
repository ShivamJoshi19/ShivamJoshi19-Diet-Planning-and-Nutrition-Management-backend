from fastapi import FastAPI, APIRouter, status
from services import user_profile, diet_management
from dto.request_dto import (user_authentication_request_dto, user_query_request_dto,
                             diet_management_request_dto)
from dto.response_dto import response_dto
from custom_utils import custom_utils

router = APIRouter()
app = FastAPI()


@router.post("/profile/", response_model=response_dto.ResponseDto)
async def UserProfile(request: user_authentication_request_dto.UserProfileDto):
    try:
        data = user_profile.UserProfileService.profile_user(request.user_id, request.first_name,
                                                            request.last_name, request.age, request.weight,
                                                            request.height, request.gender)
        response = response_dto.ResponseDto(
            Data={
                "user_id": data.get("user_id")
            },
            Success=True,
            Message=data["message"],
            Status=status.HTTP_200_OK,
        )
    except custom_utils.CustomException as e:
        response = response_dto.ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=e.status_code
        )
    except Exception as e:
        response = response_dto.ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response


@ router.post("/get-profile/", response_model=response_dto.ResponseDto)
async def login(request: user_authentication_request_dto.UserGetProfileDto):
    try:
        data = user_profile.UserProfileService.get_user_profile(
            request.user_id)
        response = response_dto.ResponseDto(
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
        response = response_dto.ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=e.status_code
        )
    except Exception as e:
        response = response_dto.ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response


@router.post("/send-query/", response_model=response_dto.ResponseDto)
async def send_user_query(request: user_query_request_dto.UserQueryRequestDto):
    try:
        data = user_profile.UserProfileService.send_user_query(
            request.user_id, request.allergic_to_food,
            request.preference, request.disease, request.diet_plan, request.query_message)
        response = response_dto.ResponseDto(
            Data={
                "dietitian_email": data["dietitian_email"],
                "user_email": data["user_email"],
                "user_id": data["user_id"],
                "first_name": data["first_name"]
            },
            Success=True,
            Message=data["message"],
            Status=status.HTTP_200_OK,
        )
    except custom_utils.CustomException as e:
        response = response_dto.ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=e.status_code
        )
    except Exception as e:
        response = response_dto.ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response


@router.get("/query-status/{id}", response_model=response_dto.ResponseDto)
async def get_query_status(id: str):
    try:
        data = user_profile.UserProfileService.get_query_status(id)
        response = response_dto.ResponseDto(
            Data={
                "query_status": data.get("query_status")
            },
            Success=True,
            Message=data["message"],
            Status=status.HTTP_200_OK,
        )
    except custom_utils.CustomException as e:
        response = response_dto.ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=e.status_code
        )
    except Exception as e:
        response = response_dto.ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response


@router.post("/diet-progress/", response_model=response_dto.ResponseDto)
async def submit_diet_progress(request: diet_management_request_dto.DietTrackRequest):
    try:
        data = diet_management.DietManager.submit_diet_progress(request.user_id, request.breakfast,
                                                                request.lunch, request.dinner, request.water_intake,
                                                                request.exercise)
        response = response_dto.ResponseDto(
            Data={
                "user_id": data.get("user_id")
            },
            Success=True,
            Message=data["message"],
            Status=status.HTTP_200_OK,
        )
    except custom_utils.CustomException as e:
        response = response_dto.ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=e.status_code
        )
    except Exception as e:
        response = response_dto.ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response


@router.get("/diet-progress/{id}", response_model=response_dto.ResponseDto)
async def get_user_diet_progress(id: str):
    try:
        data = diet_management.DietManager.get_user_diet_progress(id)
        response = response_dto.ResponseDto(
            Data={
                "user_id": data.get("user_id"),
                "plan_duration": data.get("plan_duration"),
                "diet_followed_for_days": data.get("diet_followed_for_days"),
                "progress": data.get("progress")
            },
            Success=True,
            Message="Diet Progress Fetched Successfully!",
            Status=status.HTTP_200_OK,
        )
    except custom_utils.CustomException as e:
        response = response_dto.ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=e.status_code
        )
    except Exception as e:
        response = response_dto.ResponseDto(
            Data=None,
            Success=False,
            Message=str(e),
            Status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response
