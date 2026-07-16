from llm import ask
from presence.hackatime import today
from presence.git_stats import (
    get_branch,
    get_commits_today,
    get_last_commit,
    get_diff,
    get_status
)

def build_focus():
    status = today()

    if status is None:
            return "No se ha podido obtener la actividad"
    
    total = status["total_seconds"]

    hours = total // 3600
    minutes = (total % 3600) // 60

    branch = get_branch()
    commits = get_commits_today()
    last_commit = get_last_commit()
    diff = get_diff()
    status = get_status()


    prompt = f"""
Eres Axios.

Este es el estado actual:

Proyecto: Axios
Rama: {branch}
Tiempo hoy: {hours}h {minutes}m
Commits hoy: {commits}
Último commit:
{last_commit}
Git status:
{status}
git diff: 
{diff}

Escribe:

- Un resumen muy corto.
- En qué parece que está trabajando Asier.
- Qué debería hacer después.

Máximo 60 palabras.
"""
    advice = ask(prompt)

    return f"""🎯 *Focus*

💻 *Proyecto*
Axios

🌿 *Rama*
{branch}

⏱ *Hoy*
{hours}h {minutes}m

📝 *Commits*
{commits}

📦 *Último commit*
{last_commit}

---

{advice}
"""