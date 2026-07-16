Aquí tienes un README más natural, sin marketing exagerado ni emojis.

# Axios
<img width="1024" height="300" alt="Sin título (9)" src="https://github.com/user-attachments/assets/d305a085-e413-42da-bc9e-3ea153eba8da" />


Axios is a Slack companion designed to feel like a persistent teammate instead of a generic chatbot.

It listens to messages in Slack, answers programming questions, keeps a persistent personality through a system prompt, and updates the user's coding progress using Hackatime.

## Features

* Slack bot using Socket Mode
* Configurable personality through `soul.md`
* Responses generated with Groq
* Hackatime progress integration
* Presence updates running in the background
* Runtime personality updates from Slack (admin only)

## Project structure

```
.
├── app.py                  # Slack application
├── llm.py                  # LLM interface
├── soul.py                 # Read/write personality
├── soul.md                 # System prompt
├── presence/
│   ├── hackatime.py
│   ├── notifier.py
│   ├── loop.py
│   └── progress.json
├── requirements.txt
└── .env
```

## Installation

Clone the repository.

```bash
git clone https://github.com/asierpernias/Axios.git
cd Axios
```

Create a virtual environment.

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies.

```bash
pip install -r requirements.txt
```

Create a `.env` file.

```env
SLACK_BOT_TOKEN=
SLACK_APP_TOKEN=
SLACK_SIGNING_SECRET=
GROQ_API_KEY=
HACKATIME_API_KEY=
SLACK_CHANNEL=
```

## Running

```bash
python app.py
```

For deployment on a VPS it is recommended to run the process inside `tmux` or under a service manager such as `systemd`.

## Personality

Axios reads its behavior from `soul.md`.

Every request is sent together with the contents of this file as the system prompt, making it easy to change its identity or communication style without modifying the application itself.

If enabled, the administrator can also update the prompt directly from Slack.

## Model

The model is configured in `llm.py`.

Example:

```python
client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    ...
)
```

Any Groq-supported model can be used.

## License

MIT
