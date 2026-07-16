import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from soul import read, write
from llm import ask

from presence.status import build_status
from presence.focus import build_focus

from integrations.hackatime import today
from integrations.github import user_exists
from integrations.users import (
    set_hackatime,
    set_github,
)

load_dotenv()

ADMIN_ID = "U09F98XRE1G"

app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
)


@app.event("message")
def handle_message(event, say):
    print("\n========== NUEVO EVENTO ==========")
    print(event)

    if event.get("subtype"):
        print("Tiene subtype, ignorando.")
        return

    text = event.get("text", "").strip()

    print(f"TEXT RAW: {repr(text)}")

    if not text.lower().startswith("axios"):
        print("No empieza por 'axios'")
        return

    question = text[5:].strip()

    print(f"QUESTION: {repr(question)}")

    if not question:
        print("Pregunta vacía")
        return

    parts = question.split(maxsplit=1)

    print(f"PARTS: {parts}")

    cmd = parts[0].lower()
    args = parts[1].strip() if len(parts) > 1 else ""

    print(f"CMD = {repr(cmd)}")
    print(f"ARGS = {repr(args)}")

    if cmd == "status":
        print(">>> STATUS")
        say(
            text=build_status(event["user"]),
            thread_ts=event.get("thread_ts") or event["ts"],
        )
        return

    if cmd == "focus":
        print(">>> FOCUS")
        say(
            text=build_focus(event["user"]),
            thread_ts=event.get("thread_ts") or event["ts"],
        )
        return

    if cmd == "link":
        print(">>> LINK")

        if not args:
            say(
                text=(
                    "🔗 Para vincular tu cuenta de Hackatime ejecuta:\n\n"
                    "axios link TU_API_KEY"
                ),
                thread_ts=event.get("thread_ts") or event["ts"],
            )
            return

        stats = today(args)

        print("Hackatime:", stats)

        if stats is None:
            say(
                text="❌ API Key inválida.",
                thread_ts=event.get("thread_ts") or event["ts"],
            )
            return

        set_hackatime(event["user"], args)

        say(
            text="✅ Cuenta de Hackatime vinculada correctamente.",
            thread_ts=event.get("thread_ts") or event["ts"],
        )
        return

    if cmd == "github":
        print(">>> GITHUB")

        if not args:
            say(
                text=(
                    "🐙 Para vincular GitHub ejecuta:\n\n"
                    "axios github TU_USUARIO"
                ),
                thread_ts=event.get("thread_ts") or event["ts"],
            )
            return

        print("Comprobando usuario:", args)

        if not user_exists(args):
            print("Usuario inexistente")
            say(
                text="❌ Ese usuario de GitHub no existe.",
                thread_ts=event.get("thread_ts") or event["ts"],
            )
            return

        print("Usuario válido")

        set_github(event["user"], args)

        say(
            text=f"✅ GitHub vinculado correctamente: {args}",
            thread_ts=event.get("thread_ts") or event["ts"],
        )
        return

    if cmd == "alma":
        print(">>> ALMA")

        if event["user"] != ADMIN_ID:
            say("Solo Asier puede modificar mi alma.")
            return

        if not args:
            say("Indica cómo quieres modificar mi personalidad.")
            return

        new_soul = ask(
            f"""
Esta es tu personalidad:

{read()}

Modifícala siguiendo esta instrucción:

{args}

Devuelve únicamente el nuevo markdown.
"""
        )

        write(new_soul)

        say("✅ Mi alma ha sido actualizada.")
        return

    print(">>> ASK NORMAL")

    answer = ask(question)

    say(
        text=answer,
        thread_ts=event.get("thread_ts") or event["ts"],
    )


if __name__ == "__main__":
    from threading import Thread
    from presence.loop import run

    Thread(
        target=run,
        daemon=True,
    ).start()

    handler = SocketModeHandler(
        app,
        os.getenv("SLACK_APP_TOKEN"),
    )

    handler.start()