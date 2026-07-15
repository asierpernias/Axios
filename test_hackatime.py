import os, requests 
from dotenv import load_dotenv

load_dotenv()

url = "https://hackatime.hackclub.com/api/hackatime/v1/users/current/statusbar/today"

headers = {
    "Authorization": f"Bearer {os.getenv('HACKATIME_API_KEY')}"
}

r = requests.get(url, headers = headers)

print(r.status_code)
print(r.json())