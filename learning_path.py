from typing import Literal
from gemini_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: Literal["beginner", "intermediate", "advanced"] = "beginner",
) -> str:
    prompt = f"""
Create a structured learning path for the topic "{topic}" for a {level} learner.

Include:
1. A short goal for the learner.
2. A sequence from foundational concepts toward advanced concepts.
3. Suggested time ranges for each stage.
4. Practical exercises or projects.
5. Suggested resource types such as official documentation, articles,
   books, courses, or videos. Do not invent exact URLs.
6. A simple way to check readiness before moving to the next stage.

Adapt the depth and vocabulary to the learner level. Use Markdown headings
and bullet lists so the result is easy to read.
""".strip()
    return generate_text(prompt, temperature=0.35)
