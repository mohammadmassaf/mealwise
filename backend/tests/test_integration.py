import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_full_meal_plan_flow():
    response = client.post(f"/meals/preferences",json ={"days": 3})
    assert response.status_code == 200
    id = response.json()["id"]
    meal = client.get(f"/meals/meal-plan/{id}")
    assert meal.status_code == 200
    regenerated = client.post(f"/meals/meal-plan/{id}/regenerate-day" , json = {"day": 1, "preferences": {"days": 1}})
    assert regenerated.status_code == 200
