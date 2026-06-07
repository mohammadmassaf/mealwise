from pydantic import BaseModel
from typing import Optional
from datetime import date     


class Meal(BaseModel):
    name: str   
    ingredients: list[str] 
    calories: int
    time_to_cook: Optional[int]  
    recipe: Optional[str] = None
    pass

class DayPlan(BaseModel):
    day:str
    meals:list[Meal]
    pass

class MealPlan(BaseModel):
    num_days:int
    start_date: Optional[date] = None
    plan:list[DayPlan]

class PreferenceRequest(BaseModel):
        prep_time: Optional[int] = 45
        allergies: Optional[list[str]] = None
        cuisines: Optional[list[str]] = None
        days: int
        calories_per_day:Optional[int] = 2300
        diet:Optional[str] = None
        start_date: Optional[date] = None
        
class RegenerateDayRequest(BaseModel):
     day:int
     preferences: PreferenceRequest

class PlanResponse(BaseModel):
        id: str
        plan: MealPlan
class ErrorResponse(BaseModel):
     message:str
     status_code: int 
