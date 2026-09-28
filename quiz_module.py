import json
from schemas import QuizResponse
from gemini_client import generate_structured


def clean_json_block(value: str) -> str:
    value = value.strip()
    if value.startswith("```"):
        lines = value.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        value = "\n".join(lines).strip()
    return value


def generate_quiz(passage: str) -> dict:
    prompt = f"""
Create exactly three multiple-choice questions from the educational passage below.

Requirements:
- Exactly 3 questions.
- Exactly 4 options per question.
- Only one option is correct.
- The correct_answer must exactly match one option.
- Include a short explanation for the correct answer.
- Questions must test understanding of the supplied passage, not unrelated facts.

Passage:
{passage}
""".strip()

    raw = generate_structured(prompt, QuizResponse)
    try:
        data = QuizResponse.model_validate_json(clean_json_block(raw))
    except Exception as exc:
        # Keep the original module's explicit parsing/error behavior while
        # exposing a useful server-side exception to FastAPI.
        raise RuntimeError(f"Could not parse Gemini quiz JSON: {exc}") from exc

    return {"questions": [question.model_dump() for question in data.questions]}
