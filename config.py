from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    app_name: str = "EduGenie"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"
    ai_provider: str = "gemini"
    explanation_provider: str = "gemini"
    local_explanation_model: str = "MBZUAI/LaMini-Flan-T5-783M"
    max_input_chars: int = 20000

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()