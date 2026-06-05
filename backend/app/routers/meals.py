import uuid 
from fastapi import APIRouter, HTTPException
from app.models.meal import MealPlan, PreferenceRequest, RegenerateDayRequest,PlanResponse
from app.services.planner import generate_meal_plan
from app.exceptions import GeminiUnavailableError


router = APIRouter(prefix="/meals", tags=["meals"])


meal_plans: dict[str, MealPlan] = {}

@router.post("/preferences", response_model=PlanResponse)
async def plan_meals(request: PreferenceRequest):
    try:
        result = generate_meal_plan(request)
        plan_id = str(uuid.uuid4()) 
        meal_plans[plan_id] =result
        return PlanResponse(id = plan_id , plan = result)
    except GeminiUnavailableError:
        raise HTTPException(status_code=503, detail="Gemini service is currently unavailable")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    