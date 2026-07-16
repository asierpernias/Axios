
# Axios ![Hackatime Badge](https://hackatime.hackclub.com/api/v1/badge/U09F98XRE1G/asierpernias/Axios)
<img width="1024" height="300" alt="Sin título (9)" src="https://github.com/user-attachments/assets/d305a085-e413-42da-bc9e-3ea153eba8da" />


Axios is a Slack companion designed to feel like a persistent teammate instead of a generic chatbot.

It listens to messages in Slack, answers programming questions, keeps a persistent personality through a system prompt, and tracks coding activity through Hackatime and GitHub integrations.

## Features

* Slack bot using Socket Mode
* Configurable personality through `soul.md`
* Responses generated with Groq
* Persistent user system
* Hackatime OAuth integration
* GitHub account linking
* Coding progress and presence updates
* Status and focus information
* Runtime personality updates from Slack (admin only)

## Project structure

```

.
├── app.py                  # Slack application
├── llm.py                  # LLM interface
├── soul.py                 # Read/write personality
├── soul.md                 # System prompt
├── users.json              # Linked user data
│
├── integrations/
│   ├── users.py            # User management
│   ├── hackatime.py        # Hackatime integration
│   └── github.py           # GitHub integration
│
├── presence/
│   ├── status.py
│   ├── focus.py
│   ├── git_stats.py
│   ├── notifier.py
│   └── loop.py
│
├── web/
│   └── auth.py              # OAuth callbacks
│
├── requirements.txt
└── .env

````

## Installation

Clone the repository.

```bash
git clone https://github.com/asierpernias/Axios.git
cd Axios
````

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

HACKATIME_CLIENT_ID=
HACKATIME_CLIENT_SECRET=
HACKATIME_REDIRECT_URI=

SLACK_CHANNEL=
```

## Running

```bash
python app.py
```

For deployment on a VPS it is recommended to run the process inside `tmux` or under a service manager such as `systemd`.

Axios starts both the Slack Socket Mode listener and the background presence system.

## Slack commands

Axios reacts to messages starting with:

```
axios
```

Examples:

```
axios status
```

Shows the user's current coding activity.

```
axios focus
```

Shows the user's current development focus.

```
axios link
```

Starts the Hackatime account linking process.

```
axios github username
```

Links a GitHub account to the Slack user.

The GitHub and Hackatime data is stored per Slack user.

## Hackatime OAuth

Axios uses Hackatime OAuth instead of sharing API keys directly.

The OAuth callback requires a public URL:

```
https://your-domain.com/auth/callback
```

For development, a temporary Cloudflare Tunnel can be used:

```bash
cloudflared tunnel --url http://localhost:8080
```

The generated URL must match the redirect URI configured in the Hackatime OAuth application.

## Personality

Axios reads its behavior from `soul.md`.

Every request is sent together with the contents of this file as the system prompt, making it easy to change its identity or communication style without modifying the application itself.

The administrator can also update the prompt directly from Slack.

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

## Security

The following files should never be committed:

```
.env
users.json
```

They contain tokens and linked account information.

Add them to `.gitignore`.

## License

MIT
