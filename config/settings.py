import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "").strip()
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5.4-mini").strip()

settings = Settings()

def validate_settings() -> tuple[bool, str]:
    if not settings.openai_api_key:
        return False, "OPENAI_API_KEY is missing. Add it to your local .env file."
    return True, ""
