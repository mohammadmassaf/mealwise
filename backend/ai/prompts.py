def build_meal_plan_prompt(preferences: dict) -> str:
    system_prompt = "You are a professional nutritionist and meal planning expert."

    user_prompt = f"""Create a personalized 7-day meal plan for me based on my profile:

- Diet type: {preferences['diet']}
- Allergies: {preferences['allergies']}
- Daily calorie target: {preferences['calories']}
- Preferred cuisines: {preferences['cuisines']}

For each day, provide breakfast, lunch, dinner, and a snack.
Make sure every meal:
  - Respects my diet type and avoids my allergens
  - Fits within my daily calorie target (if specified)
  - Incorporates my preferred cuisines where possible

Return your response as a JSON object only. 
No extra text, no markdown, no explanation.
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
      "total_calories": 2450
    }}
  ]
}}
"""
    return system_prompt, user_prompt