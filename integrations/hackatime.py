import requests

URL = "https://hackatime.hackclub.com/api/hackatime/v1/users/current/statusbar/today"


def today(api_key):
    if not api_key:
        return None

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    r = requests.get(
        URL,
        headers=headers,
        timeout=10,
    )

    print(r.status_code)
    print(r.text)

    if r.status_code != 200:
        return None

    data = r.json()

    return data["data"]["grand_total"]