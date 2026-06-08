from sqlalchemy.orm import Session
from app.models.meal import MealPlan
from app.models.db_models import Users, MealPlan as MealPlanDB, DayPlan as DayPlanDB, Meal as MealDB, Ingredients as IngredientsDB
from datetime import date

def save_meal_plan(db: Session, meal_plan_data: MealPlan ) -> MealPlanDB:
     start = meal_plan_data.start_date or date.today()
     meal_plan = MealPlanDB(num_days=meal_plan_data.num_days, start_date=start, user_id=None)

     for plan in meal_plan_data.days:
          day_plan = DayPlanDB(day = plan.day )
          for day in plan.meals:
               meal = MealDB(name = day.name  , calories = day.calories , time_to_cook = day.time_to_cook , recipe= day.recipe)
               for ing in day.ing:
                    ingredient = IngredientsDB(name = ing.name   )
                    meal.ing.append(ingredient)
               day_plan.meals.append(meal)
          meal_plan.days.append(day_plan)
     db.add(meal_plan)
     db.commit()
     db.refresh(meal_plan)
     return meal_plan
def get_plan(db: Session , plan_id : int) -> MealPlanDB:
     plan = db.get(MealPlanDB , plan_id)
     return plan

def  build_day_plan(day_data):
     day_plan = DayPlanDB(day = day_data.day)

     for meals in day_data.meals:
          meal = MealDB(name = meals.name  , calories = meals.calories , time_to_cook = meals.time_to_cook , recipe= meals.recipe)
          for ing in meals.ing:
                    ingredient = IngredientsDB(name = ing.name)
                    meal.ing.append(ingredient)
          day_plan.meals.append(meal)
     return day_plan