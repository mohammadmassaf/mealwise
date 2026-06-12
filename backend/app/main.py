from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import meals, auth
from app.exceptions import GeminiUnavailableError
from app.core.config import settings

app = FastAPI(title="Mealwise API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meals.router)
app.include_router(auth.router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.exception_handler(GeminiUnavailableError)
async def gemini_unavailable_handler(request: Request ,exc: GeminiUnavailableError):
    return JSONResponse(status_code = 503 , content = "Gemini service is currently unavailable")