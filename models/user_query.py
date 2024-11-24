from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone


class UserQueryModel(BaseModel):
    user_id: str = Field(...)
    first_name: str = Field(...)
    allergic_to_food: Optional[str] = Field(
        None, description="Allergies to specific foods")
    preference: str = Field(...,
                            description="Dietary preference (e.g., vegetarian, non-vegetarian)")
    disease: Optional[str] = Field(
        None, description="Any diseases the user is suffering from")
    diet_plan: str = Field(...,
                           description="Diet plan suggestions (e.g., lose weight, gain weight)")
    query_message: Optional[str] = Field(
        None, description="Custom message from the user for the dietitian"
    )
    status: str = Field(
        default="pending", description="Status of the query (e.g., pending, resolved)"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = Field(default=True)
