import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from soul import read, write
from llm import ask
from groq import Groq
from presence.status import build_status
from presence.focus import build_focus
load_dotenv()


ADMIN_ID = "U09F98XRE1G"

app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
)


@app.event("message")
def handle_mention(event, say):
    if event.get("subtype"):
        return

    text = event.get("text", "")

    if not text.lower().startswith("axios"):
        return

    question = text[5:].strip()
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
    
    cmd = question.lower().strip()

    print(cmd)

    if cmd == "status":
        print("Status detectado")
        say(
            text=build_status(),
            thread_ts=event.get("thread_ts") or event["ts"],
        )
        return
    if cmd == "focus":
        print("FOcus0")
        say(
            text=build_focus(),
            thread_ts=event.get("thread_ts") or event["ts"]
        )
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
