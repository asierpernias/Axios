from integrations.users import (
    get_hackatime,
)

from integrations.hackatime import today

def build_status(slack_id: str):
    api_key = get_hackatime(slack_id)

    if api_key is None:
        return(
            "❌ No has vinculado tu cuenta de Hackatime.\n\n"
            "Ejecuta:\n"
            "`axios link TU_API_KEY`"
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

    return f"""🤖 *Axios Status*

⏱ *Today*
{hours}h {minutes}m
    
    """