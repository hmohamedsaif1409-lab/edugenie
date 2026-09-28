from functools import lru_cache

from config import settings
from gemini_client import generate_text


def _gemini_explanation(concept: str) -> str:
    prompt = f"""
Explain the following educational concept to a beginner.

Concept:
{concept}

Requirements:
1. Start with a simple definition.
2. Explain the idea using plain language.
3. Give one intuitive example or analogy.
4. Mention one common misunderstanding if relevant.
5. Keep it concise but complete.
""".strip()
    return generate_text(prompt, temperature=0.25)


@lru_cache(maxsize=1)
def _get_local_generator():
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise RuntimeError(
            "Local explanation requires the optional dependencies in "
            "requirements-local.txt. Either install them or set "
            "EXPLANATION_PROVIDER=gemini."
        ) from exc

    return pipeline(
        "text2text-generation",
        model=settings.local_explanation_model,
    )


def _local_explanation(concept: str) -> str:
    generator = _get_local_generator()
    prompt = (
        "Explain this educational concept simply for a beginner: "
        f"{concept}"
    )
    result = generator(prompt, max_new_tokens=180, do_sample=False)
    return result[0]["generated_text"].strip()


def explain_concept(concept: str) -> str:
    provider = settings.explanation_provider.lower()
    if provider == "local":
        return _local_explanation(concept)
    return _gemini_explanation(concept)
