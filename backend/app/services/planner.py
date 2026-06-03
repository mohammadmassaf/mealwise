from app.services.prompts import build_meal_plan_prompt
from app.core.config import get_client
from . import parser

def generate_meal_plan(preferences: dict) -> dict:
    system_prompt, user_prompt = build_meal_plan_prompt(preferences)
    client = get_client()

    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    fetcher  = lambda : client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    ).text
    return parser.call_with_retry(fetcher, days=preferences["days"])

    