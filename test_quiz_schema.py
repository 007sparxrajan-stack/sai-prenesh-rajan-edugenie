import pytest
from pydantic import ValidationError

from schemas import QuizQuestion


def test_valid_quiz_question():
    question = QuizQuestion(
        question="2 + 2 = ?",
        options=["1", "2", "3", "4"],
        correct_answer="4",
        explanation="Two plus two equals four.",
    )
    assert question.correct_answer == "4"


def test_invalid_correct_answer():
    with pytest.raises(ValidationError):
        QuizQuestion(
            question="2 + 2 = ?",
            options=["1", "2", "3", "4"],
            correct_answer="5",
            explanation="Invalid answer.",
        )
