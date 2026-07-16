from pathlib import Path
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

soul = Path("soul.md")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def read():
    return soul.read_text(encoding="utf-8")


def ask(prompt: str) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
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
        max_completion_tokens=600,
        reasoning_effort="low"
    )

    message = response.choices[0].message
    if message.content:
        return message.content.strip()

    return ""
