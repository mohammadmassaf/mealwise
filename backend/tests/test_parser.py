import pytest
from mealwise.backend.app.services import parser

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
            parser.validate_meal_plan({})

def test_wrong_number_of_days():
        invalidDict = make_invalid_plan()
        with pytest.raises(ValueError):
            parser.validate_meal_plan(invalidDict)   

def test_valid_JSON_Format():
    result = parser.parse_llm_response('```json {"week": []}```')
    assert isinstance(result,dict)
    assert "week" in result

def test_Value_error():
     with pytest.raises(ValueError):
          parser.parse_llm_response('{"week": []}')

def test_fence_stripping():
    fenced   = parser.parse_llm_response('```json\n{"week": []}\n```')
    unfenced = parser.parse_llm_response('{"week": []}')
    assert fenced == unfenced