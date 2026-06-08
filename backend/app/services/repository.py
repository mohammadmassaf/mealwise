from sqlalchemy.orm import Session
from app.models.meal import MealPlan
from app.models.db_models import Users, MealPlan as MealPlanDB, DayPlan as DayPlanDB, Meal as MealDB, Ingredients as IngredientsDB


def save_meal_plan(db: Session, meal_plan_data: MealPlan) -> MealPlan:
     meal_plan = MealPlanDB(num_days=meal_plan_data.num_days, start_date=meal_plan_data.start_date, user_id=None)


     for plan in meal_plan_data.plan:
          day_plan = DayPlanDB(day = plan.day )
          for day in plan.meals:
               meal = MealDB(name = day.name  , calories = day.calories , time_to_cook = day.time_to_cook , recipe= day.recipe)
               for ing in day.ingredients:
                    ingredient = IngredientsDB(name = ing)
                    meal.ing.append(ingredient)
               day_plan.meals.append(meal)
          meal_plan.days.append(day_plan)
     db.add(meal_plan)
     db.commit()
     db.refresh(meal_plan)
     return meal_plan