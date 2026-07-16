from presence.hackatime import today
from presence.git_stats import (
    get_branch,
    get_commits_today,
    changed_files,
    get_last_commit,
)

def build_status():
    status = today()

    if status is None:
        return "No se pudo obtener la actividad"
    
    total = status["total_seconds"]

    hours = total // 3600
    minutes = (total % 3600) // 60

    return  f"""🤖 *Axios Status*

⏱ *Today*
{hours}h {minutes}m

🌿 *Branch*
{get_branch()}

📝 *Commits*
{get_commits_today()}

💻 *Files changed*
{changed_files()}

📦 *Last commit*
{get_last_commit()}
"""