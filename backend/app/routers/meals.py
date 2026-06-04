from fastapi import APIRouter, HTTPException
from app.models.meal import MealPlan, PreferenceRequest, RegenerateDayRequest
from app.services.planner import generate_meal_plan

router = APIRouter(prefix="/meals", tags=["meals"])

@router.post("/plan", response_model=MealPlan)
async def plan_meals(request: PreferenceRequest):
    preferences = request.model_dump(exclude_none=True)
    try:
        result = generate_meal_plan(preferences)
        return MealPlan(plan=[result], days=request.days)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))