import asyncio
from app.services.prompts import build_meal_plan_prompt
from app.core.config import get_client
from . import parser
from app.models.meal import  PreferenceRequest,MealPlan
from app.services.repository import save_meal_plan
from sqlalchemy.orm import Session
from app.models.db_models import Users
 

async def generate_meal_plan(request: PreferenceRequest,db:Session ,user_id : int) -> MealPlan:
    system_prompt, user_prompt = build_meal_plan_prompt(request)
    client = get_client()

    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    fetcher  = lambda : client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    ).text
    result = await asyncio.to_thread(parser.call_with_retry, fetcher, days=request.days) 
    meal_plan = parser.dict_to_meal_plan(result)
    return meal_plan,save_meal_plan(db,meal_plan,user_id)

    