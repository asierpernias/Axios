import time
import json
from pathlib import Path

from presence.hackatime import today
from llm import ask
from presence.notifier import send


FILE = Path("presence/progress.json")


def load():
    if not FILE.exists():
        return {
            "last_hour": 0
        }

    with open(FILE, "r") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)


def run():
    while True:

        stats = today()

        if stats is None:
            time.sleep(300)
            continue

        hours = int(stats["total_seconds"] // 3600)

        progress = load()

        print("Horas:", hours)
        print("Última hora avisada:", progress["last_hour"])

        if hours != progress["last_hour"] and hours != 0:

            message = ask(
                f"""
Eres Axios.

Asier acaba de completar {hours} horas programando.

Escribe un mensaje corto, motivacional y divertido.
Debe sonar como un asistente personal con personalidad propia.
Máximo 25 palabras.
Incluye un emoji si queda natural.
"""
            )

            print("DEBUG MESSAGE:", repr(message))

            if message:
                send(message)
            else:
                print("Groq no devolvió mensaje")

            progress["last_hour"] = hours
            save(progress)

        time.sleep(300)
