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
        result =await  generate_meal_plan(request)
        plan_id = str(uuid.uuid4()) 
        meal_plans[plan_id] =result
        return PlanResponse(id = plan_id , plan = result)
    except GeminiUnavailableError:
        raise HTTPException(status_code=503, detail="Gemini service is currently unavailable")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/meal-plan/{id}")
async def get_meal_plan(id:str)-> MealPlan:
    try:
        return meal_plans[id]
    except KeyError:
        raise HTTPException(status_code=404,detail=  "id not found")
    
@router.post("/meal-plan/{id}/regenerate-day")
async def regenerate_day(id: str, request: RegenerateDayRequest) ->MealPlan:
    if id not in meal_plans:
        raise HTTPException(status_code=404, detail="Plan not found")
    meal = meal_plans[id]
    request.preferences.days = 1
    try:
        result = await generate_meal_plan(request.preferences)
        meal.plan[request.day - 1] = result.plan[0]
        meal_plans[id] = meal
        return meal
    except GeminiUnavailableError:
        raise HTTPException(status_code=503, detail="Gemini service is currently unavailable")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    