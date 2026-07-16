from slack_sdk import WebClient
from dotenv import load_dotenv
import os

load_dotenv()

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

def update_status(text:str, emoji=":computer:"):
    client.users_profile_set(
        profile={
            "status_text": text[:100],
            "status_emoji": emoji,
        }
    )