from integrations.users import get_hackatime
from integrations.hackatime import today
from llm import ask

def build_focus(slack_id: str):
    api_key = get_hackatime(slack_id)

    if api_key is None:
        return (
            "❌ No has vinculado tu cuenta de Hackatime.\n\n"
            "Ejecuta:\n"
            "`axios link TU_API_KEY`"
        )
    
    stats = today(api_key)

    if stats is None:
        return "No he podido obetener tu actividad"
    
    total = stats["total_seconds"]

    hours = total // 3600
    minutes = (total % 3600) // 60

    return ask(
              f"""
El usuario lleva hoy {hours} horas y {minutes} minutos programando.

Escribe un mensaje corto motivador.
Máximo 35 palabras.
"""
    )