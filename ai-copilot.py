from dotenv import load_dotenv
from google import genai
import os

from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found.")
    
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="You are an AI career mentor. The candidate is a Process Automation Engineer skilled in Python, APIs, ETL, pandas and cloud technologies. Suggest three AI projects that would impress recruiters."
)

print(response.text)

