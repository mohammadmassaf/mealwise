from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from app.routers import meals
from app.exceptions import GeminiUnavailableError

app = FastAPI(title="Mealwise API")

app.include_router(meals.router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.exception_handler(GeminiUnavailableError)
async def gemini_unavailable_handler(request: Request ,exc: GeminiUnavailableError):
    return JSONResponse(status_code = 503 , content = "Gemini service is currently unavailable")