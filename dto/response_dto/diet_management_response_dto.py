from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class UserQueryResponse(BaseModel):
    user_id: str
    first_name: str
    allergic_to_food: Optional[str] = ""
    preference: str
    disease: Optional[str] = ""
    diet_plan: str
    query_message: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
