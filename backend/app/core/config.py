from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from google import genai
from pathlib import Path

class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
    )

    google_api_key: str
    DATABASE_URL: str
    secret_key: str
    usda_key: str
    cors_origins: str = "http://localhost:5173"

settings = Settings()

# Singleton client — initialized once at import time
_client = genai.Client(api_key=settings.google_api_key)

def get_client():
    return _client