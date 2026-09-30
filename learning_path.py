from gemini_client import generate_text


def get_learning_recommendations(topic: str, level: str = "beginner") -> str:
    prompt = f"""Create a personalized learning path for the topic "{topic}" for a {level} learner.

Organize it from beginner to advanced:
1. Prerequisites
2. Beginner concepts
3. Intermediate concepts
4. Advanced concepts
5. Practice projects or exercises
6. A suggested timeline
7. Reliable types of resources to look for (videos, documentation, books, courses)

Keep the plan practical and structured. Do not invent specific URLs.
"""
    return generate_text(prompt, temperature=0.35)
