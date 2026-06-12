from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.meal import MealPlan
from app.models.db_models import Users, MealPlan as MealPlanDB, DayPlan as DayPlanDB, Meal as MealDB, Ingredients as IngredientsDB
from datetime import date
from fastapi import HTTPException

def _build_meal(meal_data) -> MealDB:
    meal = MealDB(name=meal_data.name, calories=meal_data.calories, time_to_cook=meal_data.time_to_cook, recipe=meal_data.recipe)
    for ing in meal_data.ing:
        meal.ing.append(IngredientsDB(name=ing.name))
    return meal


def build_day_plan(day_data) -> DayPlanDB:
    day_plan = DayPlanDB(day=day_data.day)
    for meal_data in day_data.meals:
        day_plan.meals.append(_build_meal(meal_data))
    return day_plan


def save_meal_plan(db: Session, meal_plan_data: MealPlan, user_id: int) -> MealPlanDB:
    start = meal_plan_data.start_date or date.today()
    meal_plan = MealPlanDB(num_days=meal_plan_data.num_days, start_date=start, user_id=user_id)
    for day_data in meal_plan_data.days:
        meal_plan.days.append(build_day_plan(day_data))
    db.add(meal_plan)
    db.commit()
    db.refresh(meal_plan)
    return meal_plan


def get_plan(db: Session, plan_id: int) -> MealPlanDB:
    return db.get(MealPlanDB, plan_id)


def get_recent_user_plans(db: Session, user_id: int) -> list[str]:
    stmt = select(MealPlanDB).where(MealPlanDB.user_id == user_id).order_by(MealPlanDB.start_date.desc()).limit(1)
    result = db.execute(stmt).scalar_one_or_none()
    if not result:
        return []
    return [meal.name for day in result.days for meal in day.meals]

