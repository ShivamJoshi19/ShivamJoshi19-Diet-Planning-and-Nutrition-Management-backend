from typing import List
from fastapi import FastAPI, APIRouter, HTTPException, status
from services import user_profile, diet_management
from dto.request_dto import diet_management_request_dto
from dto.response_dto import response_dto, diet_management_response_dto
from custom_utils import custom_utils

router = APIRouter()
app = FastAPI()


@router.post("/create-plan/", response_model=response_dto.ResponseDto)
async def create_user_plan(request: diet_management_request_dto.DietPlanRequest):
    try:
        data = diet_management.DietManager.create_user_plan(request.user_id, request.breakfast,
                                                            request.lunch, request.dinner, request.water_intake,
                                                            request.exercise, request.plan_duration,
                                                            request.description)
        response = response_dto.ResponseDto(
            Data={
                "email": data.get("email"),
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


@router.get("/user-queries/", response_model=List[diet_management_response_dto.UserQueryResponse])
async def get_active_user_queries():
    try:
        data = diet_management.DietManager.get_active_user_queries()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
    return data


@router.get("/diet-plan/{id}", response_model=diet_management_response_dto.DietPlanResponseDto)
async def get_diet_plan(id: str):
    try:
        data = diet_management.DietManager.get_diet_plan(id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        ) from e
    return data
