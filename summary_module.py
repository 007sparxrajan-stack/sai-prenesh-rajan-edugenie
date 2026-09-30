from gemini_client import generate_text


def summarize_text(text: str, max_sentences: int = 5) -> str:
    prompt = f"""Summarize the following educational passage in at most {max_sentences} sentences.

Keep the main ideas, important facts, and relationships.
Use simple language suitable for revision.
Do not introduce information that is not in the passage.

Passage:
{text}
"""
    return generate_text(prompt, temperature=0.2)
