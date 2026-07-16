import time
import json
from pathlib import Path

from presence.hackatime import today
from llm import ask
from presence.notifier import send
from presence.profile import update_status

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

        time.sleep(300)
