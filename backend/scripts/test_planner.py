import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # ← fixes the import issue

from mealwise.backend.app.services.planner import get_user_preferences, generate_meal_plan

if __name__ == "__main__":
    prefs = get_user_preferences()
    print("\nGenerating your meal plan...\n")
    plan = generate_meal_plan(prefs)
    print("=== Your Meal Plan ===\n")
    print(plan)                    