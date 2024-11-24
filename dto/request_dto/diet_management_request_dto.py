from pydantic import BaseModel, Field


class DietPlanRequest(BaseModel):
    user_id: str = Field(...,
                         description="The ID of the user associated with the diet plan.")
    breakfast: str = Field(...,
                           description="Breakfast goal")
    lunch: str = Field(...,
                       description="Lunch goal")
    dinner: str = Field(...,
                        description="Dinner goal")
    water_intake: str = Field(...,
                              description="Water intake goal")
    exercise: str = Field(...,
                          description="Exercise goal")
    plan_duration: str = Field(..., description="Duration of the diet plan.")
    description: str = Field(..., description="Description of the diet plan.")
