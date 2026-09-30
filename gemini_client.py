from functools import lru_cache

from config import settings


class GeminiNotConfiguredError(RuntimeError):
    """Raised when GEMINI_API_KEY is not configured."""


@lru_cache(maxsize=1)
def get_client():
    if not settings.gemini_api_key:
        raise GeminiNotConfiguredError(
            "GEMINI_API_KEY is not configured. Add it to the .env file."
        )

    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError(
            "The Google GenAI SDK is not installed. Run: pip install -r requirements.txt"
        ) from exc

    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(prompt: str, *, temperature: float = 0.3) -> str:
    client = get_client()
    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config={"temperature": temperature},
    )
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
