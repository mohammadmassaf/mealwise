from pydantic import BaseModel
from typing import Optional

class MealPlanRequest(BaseModel):
    days: int
    dietary_preference: Optional[str] = None
    calories_per_day: Optional[int] = None
    cuisine: Optional[str] = None       

class MealPlanResponse(BaseModel):
    plan: str
    days: int