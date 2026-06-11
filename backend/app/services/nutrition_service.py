import httpx
from app.core.config import Settings



async def get_nutrition_data(ingredients: list[str]) -> dict:
    settings = Settings()
    api_key = settings.usda_key
    query = ", ".join(ingredients)
    try : 
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.nal.usda.gov/fdc/v1/foods/search", 
                                    params={"query":query,"pageSize": 50,"api_key":api_key})
            data = response.json()
            if response.status_code != 200:
                raise Exception(f"USDA API error: {response.status_code}")

    except httpx.HTTPError as e:
        raise Exception(f"USDA API unreachable: {e}")
    result = {}
    for food in data["foods"]:
        for nutrient  in food["foodNutrients"]:
            if nutrient["nutrientId"] == 1008:
                result[food["description"]] = nutrient["value"]
    return result 