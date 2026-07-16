import json
from pathlib import Path

FILE = Path("users.json")


def _load():
    if not FILE.exists():
        FILE.write_text("{}", encoding="utf-8")

    return json.loads(
        FILE.read_text(encoding="utf-8")
    )


def _save(data):
    FILE.write_text(
        json.dumps(data, indent=4),
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
        }

        _save(data)

    return data[slack_id]


def set_hackatime(slack_id, key):
    data = _load()

    if slack_id not in data:
        create(slack_id)

    data[slack_id]["hackatime_key"] = key

    _save(data)


def get_hackatime(slack_id):
    user = get(slack_id)

    if user is None:
        return None

    return user.get("hackatime_key")


def has_hackatime(slack_id):
    return bool(get_hackatime(slack_id))


def set_github(slack_id, username):
    data = _load()

    if slack_id not in data:
        create(slack_id)

    data[slack_id]["github_username"] = username

    _save(data)


def get_github_username(slack_id):
    user = get(slack_id)

    if user is None:
        return None

    return user.get("github_username")


def has_github(slack_id):
    return bool(get_github_username(slack_id))