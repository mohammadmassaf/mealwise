from fastapi import APIRouter, HTTPException, Depends
from app.models.meal import MealPlan, PreferenceRequest, RegenerateDayRequest, PlanResponse, PlanSummary
from app.services.planner import generate_meal_plan
from datetime import timedelta
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.services.repository import get_plan, build_day_plan, get_user_plans
from app.models.db_models import Users, DayPlan as DayPlanDB
from app.routers.auth import get_current_user

router = APIRouter(prefix="/meals", tags=["meals"])


@router.get("/my-plans", response_model=list[PlanSummary])
async def list_my_plans(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    plans = get_user_plans(db, current_user.user_id)
    return [PlanSummary(id=p.plan_id, num_days=p.num_days, start_date=p.start_date) for p in plans]


@router.post("/preferences")
async def plan_meals(request: PreferenceRequest, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        pydantic_plan, db_plan = await generate_meal_plan(request, db, current_user.user_id)
        pydantic_plan.start_date = request.start_date
        return PlanResponse(id=str(db_plan.plan_id), plan=pydantic_plan)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/meal-plan/{id}", response_model=MealPlan)
async def get_meal_plan(id: int, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    plan = get_plan(db, id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    if plan.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return plan


@router.post("/meal-plan/{id}/regenerate-day", response_model=MealPlan)
async def regenerate_day(id: int, request: RegenerateDayRequest, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    if request.day < 1:
        raise HTTPException(status_code=400, detail="Day must be 1 or greater")
    meal = get_plan(db, id)
    if meal is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    if meal.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    original_start = meal.start_date
    if original_start:
        day_date = original_start + timedelta(days=request.day - 1)
        request.preferences.start_date = day_date
    request.preferences.days = 1

    try:
        pydantic_plan, _ = await generate_meal_plan(request.preferences, db, current_user.user_id)
        # Delete the old day so its meals/ingredients are removed via cascade
        old_day = meal.days[request.day - 1]
        db.delete(old_day)
        db.flush()
        new_day = build_day_plan(pydantic_plan.days[0])
        meal.days.insert(request.day - 1, new_day)
        db.commit()
        return meal
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    