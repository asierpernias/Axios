import os
import requests 
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("HACKATIME_API_KEY")

def today():    
    url = "https://hackatime.hackclub.com/api/hackatime/v1/users/current/statusbar/today"
    print("API KEY:", USER)  
    headers = {
        "Authorization": f"Bearer {USER}"
    }

    print(headers)

    r = requests.get(url, headers=headers, timeout=10)
    
    print(r.status_code)
    print(r.text)
    if r.status_code != 200:
        print(r.text)
        return None
    
    return r.json()["data"]["grand_total"]