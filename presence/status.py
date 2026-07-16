from integrations.users import (
    get_hackatime,
)

from integrations.hackatime import today
from integrations.users import get_github_username
from integrations.github import(
    get_last_commit,
    get_commits_today,
)

def build_status(slack_id: str):
    api_key = get_hackatime(slack_id)

    if api_key is None:
        return(
            "❌ No has vinculado tu cuenta de Hackatime.\n\n"
            "Ejecuta:\n"
            "`axios link`"
        )
    stats = today(api_key)

    if stats is None:
        return (
            "❌ No he podido acceder a tu cuenta de Hackatime.\n"
            "Puede que la API Key ya no sea válida."
        )
    
    total = stats["total_seconds"]

    hours = total // 3600
    minutes = (total % 3600) // 60
    github = get_github_username(slack_id)

    github_block = ""

    if github:
        commits = get_commits_today(github)
        last = get_last_commit(github)
        github_block = f""" 

🐙 *GitHub*

👤 {github}

📝 Commits today
{commits}
"""
        if last:
            github_block += f"""

📦 Last commit

{last["repo"]}

{last["message"]}
"""

    return f"""🤖 *Axios Status*

⏱ *Today*
{hours}h {minutes}m
{github_block}
    
    """