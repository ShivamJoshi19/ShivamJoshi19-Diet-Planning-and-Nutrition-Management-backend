from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserQueryResponse(BaseModel):
    user_id: str
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    age: Optional[str] = ""
    weight: Optional[str] = ""
    height: Optional[str] = ""
    gender: Optional[str] = ""
    bmi: Optional[float] = ""
    allergic_to_food: Optional[str] = ""
    preference: str
    disease: Optional[str] = ""
    diet_plan: str
    query_message: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    is_active: bool


class DietPlanResponseDto(BaseModel):
    user_id: str
    breakfast: str
    lunch: str
    dinner: str
    water_intake: str
    exercise: str
    plan_duration: str
    description: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
