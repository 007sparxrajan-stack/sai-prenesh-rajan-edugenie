import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "EduGenie")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    request_timeout_seconds: int = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "60"))
    enable_local_explainer: bool = os.getenv("ENABLE_LOCAL_EXPLAINER", "false").lower() == "true"
    local_model_name: str = os.getenv(
        "LOCAL_MODEL_NAME", "MBZUAI/LaMini-Flan-T5-783M"
    )


settings = Settings()
