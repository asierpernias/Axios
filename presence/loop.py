import json 
import time
from llm import ask
from presence.hackatime import today
from presence.notifier import send
from presence.profile import update_status

FILE = "presence/progress.json"

def load():
    with open(FILE) as f:
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

        total_seconds = int(stats["total_seconds"]) 
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        if total_seconds >= 8*3600:
            emoji = ":trophy:"
        elif total_seconds >= 4*3600:
            emoji = ":rocket:"
        elif total_seconds >= 3600:
            emoji = ":computer:"
        else:
            emoji= ":seeding:"   

        update_status(
            f"Coding · {hours}h {minutes}m today",
            emoji
        )



        progress = load()

        if hours > progress["last_hour"]:
            message = ask(
                f""" 
Eres Axios.
Asier acaba de completar {hours} horas programando.

Escribe un mensaje corto, motivacional, divertido.
No mas de 25 palabras.
"""
            )

            send(message)

            progress["last_hour"] = hours
            save(progress)



        time.sleep(300)