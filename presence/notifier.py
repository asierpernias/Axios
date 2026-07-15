from slack_sdk import WebClient
from dotenv import load_dotenv
import os

load_dotenv()

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

CHANNEL = os.getenv("SLACK_CHANNEL")

def send(text):
    client.chat_postMessage(
        channel=CHANNEL,
        text = text,
    )