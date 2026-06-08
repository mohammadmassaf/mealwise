from pydantic import BaseModel , ConfigDict
from typing import Optional
from datetime import date     

class IngredientSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
class Meal(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str   
    ing: list[IngredientSchema] 
    calories: int
    time_to_cook: Optional[int]  
    recipe: Optional[str] = None
    pass

class DayPlan(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    day:str
    meals:list[Meal]
    pass

class MealPlan(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    num_days:int
    start_date: Optional[date] = None
    days:list[DayPlan]

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
