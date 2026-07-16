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

from integrations.link import (
    start,
    waiting,
    finish,
)

load_dotenv()


ADMIN_ID = "U09F98XRE1G"


app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
)


@app.event("message")
def handle_message(event, say):

    if event.get("bot_id"):
        return

    if event.get("subtype"):
        return


    text = event.get("text", "").strip()

    print("MENSAJE:", repr(text))


    if not text:
        return


    bot_id = app.client.auth_test()["user_id"]

    text = text.replace(
        f"<@{bot_id}>",
        ""
    ).strip()


    if waiting(event["user"]):

        key = text.strip()

        print("Validando Hackatime key")

        stats = today(key)

        if stats is None:
            say(
                text="❌ Esa API key no es válida.",
                thread_ts=event["ts"],
            )
            return


        set_hackatime(
            event["user"],
            key,
        )

        finish(event["user"])


        say(
            text="✅ Hackatime vinculado correctamente.",
            thread_ts=event["ts"],
        )


        try:
            app.client.chat_delete(
                channel=event["channel"],
                ts=event["ts"],
            )
        except Exception as e:
            print(e)


        return



    if not text.lower().startswith("axios"):
        return


    question = text[5:].strip()


    if not question:
        return


    parts = question.split(maxsplit=1)

    cmd = parts[0].lower()

    args = ""

    if len(parts) > 1:
        args = parts[1].strip()


    print(
        "CMD:",
        cmd,
        "ARGS:",
        args
    )


    thread = event.get("thread_ts") or event["ts"]



    if cmd == "status":

        say(
            text=build_status(event["user"]),
            thread_ts=thread,
        )

        return



    if cmd == "focus":

        say(
            text=build_focus(event["user"]),
            thread_ts=thread,
        )

        return



    if cmd == "link":

        start(event["user"])

        say(
            text=(
                "🔗 Envíame tu Hackatime API key en este chat.\n"
                "La validaré y borraré el mensaje automáticamente."
            ),
            thread_ts=thread,
        )

        return



    if cmd == "github":

        if not args:

            say(
                text="🐙 Usa: axios github TU_USUARIO",
                thread_ts=thread,
            )

            return


        if not user_exists(args):

            say(
                text="❌ Usuario de GitHub no encontrado.",
                thread_ts=thread,
            )

            return


        set_github(
            event["user"],
            args,
        )


        say(
            text=f"✅ GitHub vinculado: {args}",
            thread_ts=thread,
        )

        return



    if cmd == "alma":

        if event["user"] != ADMIN_ID:

            say(
                text="Solo Asier puede modificar mi alma.",
                thread_ts=thread,
            )

            return


        if not args:

            say(
                text="Necesito una instrucción.",
                thread_ts=thread,
            )

            return


        new_soul = ask(
            f"""
Esta es tu personalidad:

{read()}

Modifícala siguiendo:

{args}

Devuelve únicamente el markdown.
"""
        )


        write(new_soul)


        say(
            text="✅ Alma actualizada.",
            thread_ts=thread,
        )

        return



    answer = ask(question)


    say(
        text=answer,
        thread_ts=thread,
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