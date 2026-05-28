import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

def get_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in .env")
    
    client = genai.Client(api_key=api_key)
    return client