from functools import lru_cache

from config import settings
from gemini_client import generate_text


def _gemini_explanation(topic: str, level: str) -> str:
    prompt = f"""You are an educational tutor.

Explain the following topic for a {level} learner:
{topic}

Requirements:
- Start with a one-sentence definition.
- Break the idea into 3-6 simple points.
- Give one practical or everyday example when appropriate.
- Avoid unnecessary jargon.
- If the topic involves a formula, explain the symbols.
"""
    return generate_text(prompt, temperature=0.25)


@lru_cache(maxsize=1)
def _local_pipeline():
    if not settings.enable_local_explainer:
        return None

    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation is enabled, but transformers is not installed. "
            "Install requirements-local.txt or set ENABLE_LOCAL_EXPLAINER=false."
        ) from exc

    return pipeline(
        "text2text-generation",
        model=settings.local_model_name,
        device=-1,
    )


def _local_explanation(topic: str, level: str) -> str:
    pipe = _local_pipeline()
    prompt = (
        f"Explain {topic} to a {level} student in simple language. "
        "Give a short definition, key points, and one example."
    )
    result = pipe(prompt, max_new_tokens=220, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_concept(topic: str, level: str = "beginner") -> str:
    if settings.enable_local_explainer:
        try:
            return _local_explanation(topic, level)
        except Exception:
            # The cloud path keeps the app usable if the optional local model
            # is unavailable on the current machine.
            pass
    return _gemini_explanation(topic, level)
