from typing import List

from pydantic import BaseModel, Field
from gemini_client import get_client
from config import settings


class GeneratedQuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class GeneratedQuiz(BaseModel):
    questions: List[GeneratedQuizQuestion]


def generate_quiz(text: str, count: int = 3) -> dict:
    client = get_client()
    prompt = f"""Create exactly {count} multiple-choice questions from the educational passage below.

Rules:
- Each question must have exactly four options.
- Only one option may be correct.
- correct_answer must exactly match one of the four options.
- Add a brief explanation for the correct answer.
- Stay faithful to the supplied passage.
- Do not add facts that are not needed to answer the question.

Passage:
{text}
"""

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config={
            "temperature": 0.3,
            "response_mime_type": "application/json",
            "response_schema": GeneratedQuiz,
        },
    )

    parsed = response.parsed
    if parsed is None:
        raise RuntimeError("Gemini did not return valid structured quiz data.")

    data = parsed.model_dump()
    if len(data["questions"]) != count:
        raise RuntimeError(
            f"Expected {count} quiz questions, received {len(data['questions'])}."
        )
    return data
