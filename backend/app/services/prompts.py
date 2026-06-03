def build_meal_plan_prompt(preferences: dict) -> tuple:
    days = preferences.get("days", 7)
    system_prompt = "You are a professional nutritionist and meal planning expert."
    user_prompt = f"""Create a personalized {days}-day meal plan based on my profile:

- Diet type: {preferences.get('diet', 'none')}
- Allergies: {preferences.get('allergies', 'none')}
- Daily calorie target: {preferences.get('calories', 'not specified')}
- Preferred cuisines: {preferences.get('cuisines', 'none')}

Return JSON only, no markdown, no explanation.
Use this exact structure:
{{
  "week": [
    {{
      "day": "Monday",
      "meals": {{
        "breakfast": "...",
        "lunch": "...",
        "dinner": "...",
        "snack": "..."
      }},
      "total_calories": 2000
    }}
  ]
}}
"""
    return system_prompt, user_prompt