import os
import requests
from dotenv import load_dotenv

load_dotenv()


AUTH_URL = "https://hackatime.hackclub.com/oauth/authorize"
TOKEN_URL = "https://hackatime.hackclub.com/oauth/token"


def get_auth_url(slack_id):

    return (
        f"{AUTH_URL}"
        f"?client_id={os.getenv('HACKATIME_CLIENT_ID')}"
        f"&redirect_uri={os.getenv('HACKATIME_REDIRECT_URI')}"
        f"&response_type=code"
        f"&scope=profile+read"
        f"&state={slack_id}"
    )


def exchange_code(code):

    response = requests.post(
        TOKEN_URL,
        data={
            "client_id": os.getenv(
                "HACKATIME_CLIENT_ID"
            ),
            "client_secret": os.getenv(
                "HACKATIME_CLIENT_SECRET"
            ),
            "code": code,
            "redirect_uri": os.getenv(
                "HACKATIME_REDIRECT_URI"
            ),
            "grant_type": "authorization_code",
        },
        timeout=10,
    )

    if response.status_code != 200:
        print(response.text)
        return None

    return response.json()["access_token"]