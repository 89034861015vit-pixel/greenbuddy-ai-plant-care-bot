# GreenBuddy — AI Plant Care Telegram Bot

GreenBuddy is an open-source Telegram AI bot for plant care.
It helps users analyze houseplant photos, receive structured care advice, log plant health, and track progress over time.

## Problem

Plant owners often search for care advice only when a plant is already stressed. Most recommendations are generic and disconnected from the plant's history.

GreenBuddy turns plant care into a simple product loop:

photo → AI analysis → care action → health log → progress statistics

## Features

- Telegram bot interface
- Plant photo analysis with Vision AI
- Structured care recommendations
- SQLite health logging
- Multiple plant names per user
- `/stats` command with health progress chart
- Safe `.env.example` configuration
- PowerShell launch script for Windows

## Tech Stack

- Python
- aiogram
- SQLite
- OpenAI-compatible Vision API through ProxyAPI
- Matplotlib
- Telegram Bot API

## Project Structure

```text
greenbuddy-ai-plant-care-bot/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── requirements.txt
├── run.ps1
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── db.py
│   ├── vision.py
│   └── viz.py
└── docs/
    ├── roadmap.md
    ├── architecture.md
    └── database_schema.md
```

## Setup

1. Create a Telegram bot with @BotFather.
2. Copy the bot token.
3. Get a ProxyAPI key or another OpenAI-compatible API key.
4. Install Python dependencies.
5. Run the bot with PowerShell.

## Run on Windows

```powershell
pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

The script will ask for:

- `TELEGRAM_BOT_TOKEN`
- `PROXYAPI_KEY`

Do not commit real tokens to GitHub.

## Environment Variables

Use `.env.example` as a safe example file.

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
PROXYAPI_KEY=your_proxyapi_key_here
VISION_MODEL=gpt-4o-mini
```

## Why Open Source

GreenBuddy is intended as a practical reference project for small AI agents that solve everyday problems. It demonstrates Telegram UX, image analysis, persistent memory, health logging, and retention mechanics in a simple product structure.

## How Codex Can Help

Codex can help improve:

- code refactoring
- automated tests
- issue triage
- pull request review
- security checks
- release workflows
- documentation quality

## Roadmap

See `docs/roadmap.md`.

## License

MIT
