import subprocess

def _run(command):
    return subprocess.check_output(
        command,
        text=True,
    ).strip()

def get_branch():
    return _run(["git", "branch", "--show-current"])

def get_commits_today():
    return int(
        _run(
            [
                "git",
                "rev-list",
                "--count",
                "--since=00:00",
                "HEAD",
            ]
        )
    )

def changed_files():
    files = _run(
        [
            "git",
            "diff",
            "--name-only",
            "HEAD",
        ]
    )

    if not files:
        return 0
    return len(files.splitlines())

def get_last_commit():
    return _run(
        [
            "git",
            "log",
            "-1",
            "--pretty=%",
        ]
    )

def get_diff():
    return _run(
        [
            "git",
            "diff",
            "--stat",
        ]
    )
def get_status():
    return _run(
        [
            "git", 
            "status",
            "--short",
        ]
    )