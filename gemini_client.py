from google import genai
from google.genai import types

from config import settings


def _client() -> genai.Client:
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. Copy .env.example to .env "
            "and add your Google Gemini API key."
        )
    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(prompt: str, *, temperature: float = 0.3) -> str:
    client = _client()
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text


def generate_structured(prompt: str, schema: type) -> str:
    client = _client()
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty structured response.")
    return text
