# Architecture

GreenBuddy follows a simple Telegram-first AI agent flow.

## Flow

1. User sends a plant photo in Telegram.
2. Bot receives the image.
3. Vision module sends the image to an OpenAI-compatible Vision model.
4. The model returns structured JSON.
5. Database module stores plant health logs in SQLite.
6. Stats module generates a health chart.
7. User receives diagnosis, next action, and progress statistics.

## Modules

- `src/main.py` — Telegram bot handlers
- `src/config.py` — environment configuration
- `src/vision.py` — plant photo analysis
- `src/db.py` — SQLite storage
- `src/viz.py` — chart generation

## Data Loop

photo → analysis → care advice → log → statistics → better user habit
