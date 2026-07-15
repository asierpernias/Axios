import os
import requests 
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("HACKTIME_USER_ID")

def today():    
    url = "https://hackatime.hackclub.com/api/hackatime/v1/users/current/statusbar/today"

    headers = {
        "Authorization": f"Bearer {USER}"
    }

    r = requests.get(url, headers=headers, timeout=10)

    if r.status_code != 200:
        print(r.text)
        return None
    
    return r.json()["data"]["grand_total"]