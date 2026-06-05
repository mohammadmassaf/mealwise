from app.models.meal import  PreferenceRequest


def build_meal_plan_prompt(request:PreferenceRequest) -> tuple:


    preferences = request.model_dump(exclude_none=True)
    start_date = preferences.get("start_date")
    start_day = start_date.strftime("%A, %Y-%m-%d") if start_date else "Monday"   
    meal_structure = """
          {
              "name": "...",
              "ingredients": [...],
              "calories": "<integer>",
              "time_to_cook": "<integer in minutes>",
              "recipe": "Step 1: ... Step 2: ..."
          }
          """
    system_prompt = f"""You are a professional nutritionist and meal planning expert.
    Return JSON only, no markdown, no explanation.
          Use this exact structure: (Always use metric measurements (grams, ml) for all ingredients.)
          {{
            "week": [
              {{
                "day": "{start_day}",
                "meals": {{
                  "breakfast":  {meal_structure},
                  "lunch":  {meal_structure},
                  "dinner":  {meal_structure},
                  "snack":  {meal_structure}
                }},
                "total_calories": 2000
              }}
            ]
          }}
    """
    user_prompt = f"""Create a personalized {preferences.get("days")}-day meal plan based on my profile:
        - Start date: {preferences.get("start_date", "Monday")}
        - Diet type: {preferences.get("diet" , "none")}
        - Allergies: {preferences.get("allergies","none")}
        - Daily calorie target: {preferences.get("calories_per_day" , "2300")}
        - Preferred cuisines: {preferences.get("cuisines","none")}
        -preperation time : {preferences.get("prep_time", "45")}

        """
    return system_prompt, user_prompt