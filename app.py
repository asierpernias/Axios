import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from soul import read, write
from llm import ask

load_dotenv()

ADMIN_ID = "U09F98XRE1G"

app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
)

@app.event("app_mention")
def handle_mention(event, say):
    print("!")
    question = event["text"]

    if ">" in question:
        question = question.split(">", 1)[1].strip()

    if question.lower().startswith("alma"):
        if event["user"] != ADMIN_ID:
            say("Solo Asier puede modificar mi alma")
            return
        instruction = question[4:].strip()

        new_soul = ask(f"""
Esta es tu personalidad: {read()}        
Modificala siguiendo la instrucion: {instruction}
Devuelve unicamente el nuevo markdown
""")
        write(new_soul)
        say("Mi alma ha sido actualizada.")
        return
    
    answer = ask(question)

    say(   text=answer,
        thread_ts= event.get("thread_ts") or event["ts"],
    )

if __name__ == "__main__":
    handler = SocketModeHandler(
        app,
        os.getenv("SLACK_APP_TOKEN"),
    )
    from threading import Thread
    from presence.loop import run

    Thread(target=run, daemon=True).start()

    handler.start()
