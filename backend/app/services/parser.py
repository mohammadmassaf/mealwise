import json
import requests
import time 
from app.models.meal import MealPlan,Meal,DayPlan

def parse_llm_response(raw:str) -> dict:
    """
    removes '''json and ''' if they are surrounding the data
    Parses a raw JSON string returned by the LLM into a Python dict.
    Raises ValueError if the string is not valid JSON.
    """
    raw = raw.strip()
    if raw.startswith("```json") and raw.endswith("```"):
        raw = raw[7:-3].strip()
   
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
    # LLM sometimes returns malformed or non-JSON output:
        raise ValueError(f"expected data in json format : {raw}")
    return data




def validate_meal_plan(data: dict, days: int = 7) -> bool:
    if 'week' not in data:
        raise ValueError(f"data should include a key called week, received: {data}")
    if len(data["week"]) != days:
        raise ValueError(f"expected {days} days, received: {len(data['week'])}")
    for day in data["week"]:
        if "day" not in day:
            raise ValueError(f"day field missing in: {day}")
        if "meals" not in day:
            raise ValueError(f"meals field missing in: {day}")
        for meal in ["breakfast", "lunch", "dinner", "snack"]:
            if meal not in day["meals"]:
                raise ValueError(f"{meal} missing in: {day['meals']}")
    return True

def call_with_retry(func,max_retries = 3, days: int = 7):
    for attempt in range(max_retries):
        try:
            result = func()
            parsed_result = parse_llm_response(result)
            validate_meal_plan(parsed_result, days=days)
            return parsed_result
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"Max retries reached: {e}")
        

def dict_to_meal_plan(data:dict) -> MealPlan:
        days = []
        for week in data["week"]:
            meals = []
            for  meal  in week["meals"].values():
                meals.append(Meal(name=meal["name"], ingredients=meal["ingredients"],
                                   calories=meal["calories"], time_to_cook=meal["time_to_cook"], recipe= meal["recipe"]))
            days.append(DayPlan(day=week["day"], meals = meals))
        return MealPlan(num_days = len(data["week"]) , plan = days)