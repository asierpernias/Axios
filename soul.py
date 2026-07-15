from pathlib import Path

soul = Path("soul.md")

def read():
    return soul.read_text(encoding="utf-8")

def write(text):
    soul.write_text(text, encoding="utf-8")