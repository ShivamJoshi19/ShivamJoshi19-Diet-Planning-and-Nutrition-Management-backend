from pydantic import BaseModel, Field
from typing import Optional


class UserQueryRequestDto(BaseModel):
    user_id: str = Field(..., description="The unique ID of the user")
    allergic_to_food: Optional[str] = Field(
        None, description="Allergies to specific foods")
    preference: str = Field(...,
                            description="Dietary preference (e.g., vegetarian, non-vegetarian)")
    disease: Optional[str] = Field(
        None, description="Any diseases the user is suffering from")
    query_message: Optional[str] = Field(
        None, description="Custom message from the user for the dietitian")
