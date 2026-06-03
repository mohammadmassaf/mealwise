from pydantic_settings import BaseSettings
from google import genai
from pathlib import Path

class Settings(BaseSettings):
    google_api_key: str

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent.parent / ".env"

settings = Settings()

def get_client():
    return genai.Client(api_key=settings.google_api_key)