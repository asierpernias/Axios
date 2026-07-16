import requests
from datetime import datetime, timezone

BASE = "https://api.github.com"


def _get(url):
    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        return None

    return r.json()


def user_exists(username):
    return _get(f"{BASE}/users/{username}") is not None


def get_user(username):
    return _get(f"{BASE}/users/{username}")


def get_repositories(username):
    repos = _get(
        f"{BASE}/users/{username}/repos?sort=updated&per_page=100"
    )

    if repos is None:
        return []

    return repos


def get_last_repository(username):
    repos = get_repositories(username)

    if not repos:
        return None

    return repos[0]


def get_last_commit(username):
    repo = get_last_repository(username)

    if repo is None:
        return None

    commits = _get(
        repo["commits_url"].replace("{/sha}", "")
    )

    if not commits:
        return None

    commit = commits[0]

    return {
        "repo": repo["name"],
        "message": commit["commit"]["message"],
        "date": commit["commit"]["author"]["date"],
    }


def get_commits_today(username):
    repo = get_last_repository(username)

    if repo is None:
        return 0

    commits = _get(
        repo["commits_url"].replace("{/sha}", "")
    )

    if commits is None:
        return 0

    today = datetime.now(timezone.utc).date()

    total = 0

    for commit in commits:
        author = commit["commit"]["author"]["name"]

        if author.lower() != username.lower():
            continue

        date = datetime.fromisoformat(
            commit["commit"]["author"]["date"].replace("Z", "+00:00")
        ).date()

        if date == today:
            total += 1

    return total