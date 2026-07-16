import requests


URL = "https://hackatime.hackclub.com/api/v1/users/current/status"


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

    if r.status_code != 200:
        print(r.text)
        return None

    data = r.json()

    return data["data"]["grand_total"]