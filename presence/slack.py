import os 

from slack_sdk import WebClient

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

def set_status(texts: str, emoji=":headphones"):
    client.users_profile_set(
        profile={
            "status_text": texts[:100],
            "status_emoji": emoji,
        }
    )