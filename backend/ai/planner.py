from backend.ai.prompts import build_meal_plan_prompt
from backend.config import get_client

def get_user_preferences() -> dict:
    print("=== Meal Planner Setup ===\n")
    # your input() calls go here
    # return a dict like:
    # { "diet": ..., "allergies": ..., "cuisines": ..., ... }
    diet = input("diet type : ").strip() 
    allergies = input("what are your allergies (or  press Enter if none): ").strip() or "none"
    calories_raw = input("Daily calorie target (or press Enter to skip): ").strip()

    # validate it's actually a number
    if calories_raw and not calories_raw.isdigit():
        print("Invalid input, skipping calorie target.")
        calories_raw = "not specified"

    calories = calories_raw or "not specified"
    cuisines = input("what are your prefered cuisines(or press Enter if none): ").strip() or "none"
    preferences = {
        "diet": diet,
        "allergies": allergies,
        "calories":calories,    
        "cuisines": cuisines,
        
     }
    return preferences
    



def generate_meal_plan(preferences: dict) -> str:
    system_prompt, user_prompt = build_meal_plan_prompt(preferences)
    client = get_client()

    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )
    return response.text
    