from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from google import genai
from pathlib import Path

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=str(Path(__file__).resolve().parent.parent.parent.parent / ".env"))
    
    google_api_key: str
    DATABASE_URL : str
    secret_key: str
    usda_key : str

settings = Settings()

def get_client():
    return genai.Client(api_key=settings.google_api_key)