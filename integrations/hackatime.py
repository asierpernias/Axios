import requests

URL = "https://hackatime.hackclub.com/api/v1/users/current/status_bar/today"

def today(api_key):
    try:
        response = response.get(
            URL,
            headers={
                "Authorization": f"Bearer {api_key}"
            },
            timeout=10,
        )

        if response.status_code != 200:
            return None
        
        data = response.json()["data"]["grand_total"]

        return {
            "text": data["text"],
            "total_seconds": data["total_seconds"],
        }
    except Exception:
        return None