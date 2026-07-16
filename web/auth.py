from flask import Flask, request
from integrations.hackatime_oauth import exchange_code
from integrations.users import set_hackatime


app = Flask(__name__)


@app.route("/auth/callback")
def callback():

    code = request.args.get("code")
    slack_id = request.args.get("state")


    if not code:
        return "Authorization failed"


    token = exchange_code(code)


    if not token:
        return "Token exchange failed"


    set_hackatime(
        slack_id,
        token,
    )


    return """
    <h1>✅ Hackatime conectado</h1>
    Puedes volver a Slack.
    """


def run_web():

    app.run(
        host="0.0.0.0",
        port=8080,
    )