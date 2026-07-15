import os
import requests 
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("HACKTIME_USER_ID")

def today_minutes():

    try:
        r = requests.get(
            f"https://hackatime.hackclub.com/api/v1/users/{USER}/stats",
            timeout=10,
        )

        if r.status_code != 200:
            print(r.text)
            return None
        data = r.json()

        print(data)

        return None
    except Exception as e:
        print(e)
        return None
