from ollama import chat
from pathlib import Path

soul = Path("soul.md")
def ask(prompt: str) -> str:
    response = chat(
        model="phi3:latest",
        messages=[
            {
                "role": "system",
                "content": soul,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    return response["message"]["content"]
