from typing import List

from pydantic import BaseModel, Field, field_validator


class QARequest(BaseModel):
    question: str = Field(min_length=2, max_length=4000)


class ExplainRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=2000)
    level: str = Field(default="beginner", min_length=3, max_length=30)


class QuizRequest(BaseModel):
    text: str = Field(min_length=20, max_length=12000)
    count: int = Field(default=3, ge=1, le=10)


class SummaryRequest(BaseModel):
    text: str = Field(min_length=30, max_length=20000)
    max_sentences: int = Field(default=5, ge=1, le=12)


class LearningPathRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=2000)
    level: str = Field(default="beginner", min_length=3, max_length=30)


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str

    @field_validator("correct_answer")
    @classmethod
    def correct_answer_must_be_an_option(cls, value, info):
        options = info.data.get("options", [])
        if options and value not in options:
            raise ValueError("correct_answer must exactly match one option.")
        return value


class QuizResponse(BaseModel):
    questions: List[QuizQuestion] = Field(min_length=1, max_length=10)


class ErrorResponse(BaseModel):
    detail: str
