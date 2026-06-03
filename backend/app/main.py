from fastapi import FastAPI
from app.routers import meals

app = FastAPI(title="Mealwise API")

app.include_router(meals.router)

@app.get("/health")
async def health():
    return {"status": "ok"}