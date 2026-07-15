from ollama import chat
from pathlib import Path
from groq import Groq 
import os

soul = Path("soul.md")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def read():
    return soul.read_text(encoding="utf-8")
def ask(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
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
        temperature=0.8,
        max_completion_tokens=300
    )
    return response.choices[0].message.content
