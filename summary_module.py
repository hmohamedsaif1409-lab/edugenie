from gemini_client import generate_text


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational text for quick revision.

Requirements:
- Preserve the important facts and relationships.
- Remove repetition and unnecessary wording.
- Use clear, student-friendly language.
- Prefer a short heading followed by bullet points when appropriate.
- Do not add facts that are not supported by the source text.

Text:
{text}
""".strip()
    return generate_text(prompt, temperature=0.2)
