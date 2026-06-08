
from fastapi import APIRouter, HTTPException , Depends
from app.models.meal import MealPlan, PreferenceRequest, RegenerateDayRequest,PlanResponse
from app.services.planner import generate_meal_plan
from datetime import timedelta
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.services.repository import get_plan,build_day_plan


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

@router.get("/meal-plan/{id}", response_model = MealPlan)
async def get_meal_plan(id:int ,db: Session = Depends(get_db)): 
    plan = get_plan(db, id)
    if plan is None:
        raise HTTPException(status_code=404, detail="id not found")
    return plan
    
@router.post("/meal-plan/{id}/regenerate-day",response_model = MealPlan)
async def regenerate_day(id: int , request: RegenerateDayRequest, db:Session = Depends(get_db)):
    if request.day < 1:
        raise HTTPException(status_code=400, detail="Day must be 1 or greater")
    meal = get_plan(db,id)

    if meal is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    original_start = meal.start_date

    if original_start:
        day_date = original_start + timedelta(days=request.day - 1)
        request.preferences.start_date = day_date
        request.preferences.days = 1
    try:
        pydantic_plan , db_plan= await generate_meal_plan(request.preferences,db)
        meal.days[request.day - 1] = build_day_plan(pydantic_plan.days[0])
        db.commit()

        return meal
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    