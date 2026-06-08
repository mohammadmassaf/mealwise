
from fastapi import APIRouter, HTTPException , Depends
from app.models.meal import MealPlan, PreferenceRequest, RegenerateDayRequest,PlanResponse
from app.services.planner import generate_meal_plan
from datetime import timedelta
from app.core.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/meals", tags=["meals"])


meal_plans: dict[str, MealPlan] = {}

@router.post("/preferences", response_model=PlanResponse)
async def plan_meals(request: PreferenceRequest, db:Session = Depends(get_db)):
    try:
        pydantic_plan, db_plan=await  generate_meal_plan(request,db)
        pydantic_plan.start_date = request.start_date
    
        return PlanResponse(id = str(db_plan.plan_id) , plan = pydantic_plan)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/meal-plan/{id}")
async def get_meal_plan(id:str)-> MealPlan:
    try:
        return meal_plans[id]
    except KeyError:
        raise HTTPException(status_code=404,detail=  "id not found")
    
@router.post("/meal-plan/{id}/regenerate-day")
async def regenerate_day(id: str, request: RegenerateDayRequest, db:Session = Depends(get_db)) ->MealPlan:
    if id not in meal_plans:
        raise HTTPException(status_code=404, detail="Plan not found")
    meal = meal_plans[id]
    original_start = meal_plans[id].start_date
    if original_start:
        day_date = original_start + timedelta(days=request.day - 1)
        request.preferences.start_date = day_date
        request.preferences.days = 1
    try:
        result = await generate_meal_plan(request.preferences)
        meal.plan[request.day - 1] = result.plan[0]
        meal_plans[id] = meal
        return meal
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    