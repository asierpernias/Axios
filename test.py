from slack_sdk import WebClient
import os
 
print(repr(os.getenv("SLACK_BOT_TOKEN")))
client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

print(client.auth_test())

print(client.conversations_list(types="public_channel,private_channel"))
