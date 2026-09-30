from gemini_client import generate_text

SYSTEM_PROMPT = """You are EduGenie, a careful educational assistant.
Answer the student's question accurately and concisely.
Use simple language appropriate for the requested context.
When a topic is uncertain or depends on current information, say so rather than inventing facts.
Do not pretend to have browsed the web.
"""


def answer_question(question: str) -> str:
    prompt = f"""{SYSTEM_PROMPT}

Student question:
{question}

Give a direct answer first, then add a short explanation or example if useful.
"""
    return generate_text(prompt, temperature=0.2)
