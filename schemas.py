from typing import Literal
from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(min_length=1)


class QuizRequest(BaseModel):
    text: str = Field(min_length=1)


class LearningPathRequest(BaseModel):
    topic: str = Field(min_length=1)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(min_length=3, max_length=3)
