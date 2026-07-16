import json
from pathlib import Path

FILE = Path("users.json")

def _load(): 
    if not FILE.exists():
        FILE.write_text("{}", encoding="utf-8")
    return json.loads(FILE.read_text(encoding="utf-8"))

def _save(data):
    FILE.write_text(
        json.dumps(data,indent=4),
        encoding="utf-8",
    )
def get(slack_id):
    return _load().get(slack_id)

def exists(slack_id):
    return slack_id in _load()

def create(slack_id, name=None):
    data = _load()

    if slack_id not in data:
        data[slack_id] = {
            "name": name,
            "hackatime_key": None,
            "github_username": None,
            "github_token": None,
        }
        _save(data)

    return data[slack_id]

def set_hackatime(slack_id, key):
    data = _load()

    if slack_id not in data:
        create(slack_id)

    data = _load()
    data[slack_id]["hackatime_key"] = key

    _save(data)

def set_github(slack_id, username, token):
    data = _load()

    if slack_id not in data:
        create(slack_id)

    data = _load()

    data[slack_id]["github_username"] = username
    data[slack_id]["github_token"] = token

    _save(data)