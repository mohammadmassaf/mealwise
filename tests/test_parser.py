import pytest
from backend.ai import parser

def make_valid_plan():
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    return {
        "week": [
            {"day": d, "meals": {"breakfast": "x", "lunch": "x", "dinner": "x", "snack": "x"}}
            for d in days
        ]
    }
def make_invalid_plan():
    days = ["Monday","Tuesday","Wednesday"]
    return {
        "week": [
            {"day": d, "meals": {"breakfast": "x", "lunch": "x", "dinner": "x", "snack": "x"}}
            for d in days
        ]
    }


def  test_valid_meal_plan():
        dict = make_valid_plan()
        result = parser.validate_meal_plan(dict)

        assert result == True

def test_missing_week_key():

        with pytest.raises(ValueError):
            parser.validate_meal_plan(dict)

def test_wrong_number_of_days():
        invalidDict = make_invalid_plan()
        with pytest.raises(ValueError):
            parser.validate_meal_plan(invalidDict)     