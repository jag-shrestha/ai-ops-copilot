from google import genai
from config import GEMINI_API_KEY, MODEL_NAME
from pydantic import BaseModel
from google.genai import types
import time
import random

client = genai.Client(api_key=GEMINI_API_KEY)

def ask_llm(prompt, schema, max_retries=4):
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(
                model= MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                ),
            )

        except Exception as e:
            if "503" not in str(e):
                raise

            if attempt == max_retries - 1:
                raise

            wait_time = (2 ** attempt) + random.uniform(0, 1)

            print(
                f"Gemini unavailable. "
                f"Retry {attempt + 1}/{max_retries} "
                f"in {wait_time:.1f}s..."
            )

            time.sleep(wait_time)


class CountryInfo(BaseModel):
    name: str
    population: int
    capital: str
    continent: str
    gdp: int
    official_language: str
    total_area_sq_mi: int

def return_json_schema(prompt):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type='application/json',
            response_schema=CountryInfo,
        ),
    )
    return response.text

from enum import Enum

class InstrumentEnum(Enum):
    PERCUSSION = 'Percussion'
    STRING = 'String'
    WOODWIND = 'Woodwind'
    BRASS = 'Brass'
    KEYBOARD = 'Keyboard'

def return_app_json_response(prompt):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': CountryInfo,
        },
    )
    return response.text