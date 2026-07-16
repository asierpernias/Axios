import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from soul import read, write
from llm import ask
from groq import Groq
from presence.status import build_status
from presence.focus import build_focus

from integrations.users import set_hackatime
from integrations.hackatime import today
from integrations.github import user_exists
from integrations.users import set_github
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
            text=build_status(event["user"]),
            thread_ts=event.get("thread_ts") or event["ts"],
        )
        return
    if cmd == "focus":
        print("FOcus0")
        say(
            text=build_focus(event["user"]),
            thread_ts=event.get("thread_ts") or event["ts"]
        )
        return
    
    if cmd == "link":
        parts = question.split(maxsplit=1)

        if len(parts) == 1:
            say(
               text = ( "🔗 Para vincular Hackatime ejecuta:\n\n"
                "axios link TU_API_KEY"),
                thread_ts=event.get("thread_ts") or event["ts"],
            )
            return
        api_key = parts[1].strip()

        stats = today(api_key)

        if stats is None:
            say(
                text="❌ API Key inválida.",
                therad_ts=event.get("thread_ts") or event["ts"],
            )
            return
        set_hackatime(
            event["user"],
            api_key,
        )

        say(
            text="✅ Tu cuenta de Hackatime ha sido vinculada correctamente.",
            thread_ts=event.get("thread_ts") or event["ts"],
        )
        return
    
    if cmd == "github":
        parts = question.split(maxsplit=1)

        if len(parts) == 1:
            say(
                text=(
                    "🐙 Vincula tu cuenta de GitHub:\n\n"
                    "axios github TU_USUARIO"
                ),
                thread_ts=event.get("thread_ts") or event["ts"],
            )
            return

        username = parts[1].strip()

        if not user_exists(username):
            say(
                text="❌ Ese usuario de GitHub no existe.",
                thread_ts=event.get("thread_ts") or event["ts"],
            )
            return

        set_github(
            event["user"],
            username,
        )

        say(
            text=f"✅ GitHub vinculado correctamente ({username}).",
            thread_ts=event.get("thread_ts") or event["ts"],
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
