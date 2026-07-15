from ollama import chat
from pathlib import Path

soul = Path("soul.md")

def read():
    return soul.read_text(encoding="utf-8")
def ask(prompt: str) -> str:
    response = chat(
        model="phi3:latest",
        messages=[
            {
                "role": "system",
                "content": read(),
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    return response["message"]["content"]
