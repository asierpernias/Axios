import requests

BASE = "https://api.github.com"

def user_exists(username):
    r = requests.get(
        f"{BASE}/users/{username}",
        timeout=10,
    )

    return r.status_code == 200

def get_user(username):
    r = requests.get(
        f"{BASE}/users/{username}",
        timeout=10,
    )

    if r.status_code != 200:
        return None
    
    return r.json()