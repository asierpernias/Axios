import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from llm import ask

load_dotenv()

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

    answer = ask(question)

    say(   text=answer,
        thread_ts= event.get("thread_ts") or event["ts"],
    )

if __name__ == "__main__":
    handler = SocketModeHandler(
        app,
        os.getenv("SLACK_APP_TOKEN"),
    )
    handler.start()
