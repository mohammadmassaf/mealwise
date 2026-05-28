import json
import requests
import time 

def parse_llm_response(raw:str) -> dict:
    """
    removes '''json and ''' if they are surrounding the data
    Parses a raw JSON string returned by the LLM into a Python dict.
    Raises ValueError if the string is not valid JSON.
    """
    if raw.startswith("```json") and raw.endswith("```"):
        raw = raw[7:-3].strip()
   
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
    # LLM sometimes returns malformed or non-JSON output:
        raise ValueError(f"expected data in json format : {raw}")
    return data




def validate_meal_plan(data: dict) -> bool:
    """Validates the structure of a weekly meal plan dictionary.

    Args:
        data (dict): The meal plan data to validate. Expected structure:
            {
                "week": [
                    {
                        "day": "Monday",
                        "meals": {
                            "breakfast": "...",
                            "lunch": "...",
                            "dinner": "...",
                            "snack": "..."
                        }
                    },
                    ... (7 days total)
                ]
            }

    Returns:
        bool: True if the structural validation passes.

    Raises:
        ValueError: If any required keys are missing or if the data 
                    does not represent exactly 7 days.
    """
    # 1. Validate top-level structure and duration
    if 'week' not in data:
        raise ValueError(f"data should include a key called week, received: {data}")
    
    if len(data["week"]) != 7:
        raise ValueError(f"the amount of days should be 7, received: {len(data['week'])}")
    
    # 2. Validate each daily entry
    for day in data["week"]:
        if "day" not in day:
            raise ValueError(f"day field is not included in: {day}")
        
        if "meals" not in day:
            raise ValueError(f"meals field is not included in: {day}")
        
        # 3. Validate specific required meals for the day
        required_meals = ["breakfast", "lunch", "dinner", "snack"]
        for meal in required_meals:
            if meal not in day["meals"]:
                raise ValueError(f"{meal} should be inside meals: {day['meals']}")
    
    return True


def call_with_retry(func,max_retries = 3):
    for attempt in range(max_retries):
        try:
            # 1. Call function and parse/validate the result
            result = func()
            parsed_result = parse_llm_response(result)
            if(validate_meal_plan(parsed_result)):
                return parsed_result
            else:
                raise ValueError("Validation failed")

        except Exception as e : 
            # Check for 401: Give up immediately
            if "401" in str(e):
                print("401 Error: Unauthorized. Giving up immediately.")
                raise e
            # Check for 503: Exponential backoff
            elif "503" in str(e):
                if attempt == max_retries - 1:   # no more attempts left
                    raise e
                wait_time = 2 ** attempt
                print(f"503 Error: Retrying in {wait_time}s...")
                time.sleep(wait_time)
            # Handle other unexpected errors
            else:
                print(f"Unexpected error encountered: {e}")
                raise e
    raise RuntimeError("Max retry attempts reached. Operation failed.")