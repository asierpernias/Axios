import json 
import time
from presence.hacktime import today_minutes
from presence.notifier import send

FILE = "presence/progress.json"

def load():
    with open(FILE) as f:
        return json.load(f)
    
def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

def run():
    while True:

        minutes = today_minutes()

        if minutes is None:
            time.sleep(300)
            continue

        hours = minutes // 60

        progress = load()

        if hours > progress["last_hour"]:
            send(f"🎉 ¡Ya llevas {hours} horas programando hoy!")

            progress["last_hour"] = hours
            save(progress)

        time.sleep(300)