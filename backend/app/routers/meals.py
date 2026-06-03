from fastapi import APIRouter, HTTPException
from app.models.meal import MealPlanRequest, MealPlanResponse
from app.services.planner import generate_meal_plan

router = APIRouter(prefix="/meals", tags=["meals"])

@router.post("/plan", response_model=MealPlanResponse)
async def plan_meals(request: MealPlanRequest):
    preferences = {
        "days": request.days,
        "diet": request.dietary_preference,
        "calories": request.calories_per_day,
        "cuisines": request.cuisine,
        "allergies": None
    }
    
    try:
        result = generate_meal_plan(preferences)
        return MealPlanResponse(plan=str(result), days=request.days)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))