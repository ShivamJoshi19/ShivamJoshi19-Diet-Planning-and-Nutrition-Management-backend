from pydantic import BaseModel, Field
from datetime import datetime, timezone


class DietPlanModel(BaseModel):
    user_id: str = Field(...)
    breakfast: str = Field(...)
    lunch: str = Field(...)
    dinner: str = Field(...)
    water_intake: str = Field(...)
    exercise: str = Field(...)
    plan_duration: str = Field(...)
    description: str = Field(...)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=False)


class DietTrackingModel(BaseModel):
    user_id: str = Field(...)
    breakfast: str = Field(...)
    lunch: str = Field(...)
    dinner: str = Field(...)
    water_intake: str = Field(...)
    exercise: str = Field(...)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=False)
