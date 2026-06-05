import uuid 
from fastapi import APIRouter, HTTPException
from app.models.meal import MealPlan, PreferenceRequest, RegenerateDayRequest,PlanResponse
from app.services.planner import generate_meal_plan


router = APIRouter(prefix="/meals", tags=["meals"])


meal_plans: dict[str, MealPlan] = {}

@router.post("/preferences", response_model=MealPlan)
async def plan_meals(request: PreferenceRequest):
    try:
        result = generate_meal_plan(request)
        plan_id = str(uuid.uuid4()) 
        meal_plans[plan_id] =result
        
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    


    return PlanResponse(id = plan_id , plan = result)