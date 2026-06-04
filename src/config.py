from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    telegram_bot_token: str
    proxyapi_key: str
    vision_model: str = "gpt-4o-mini"
    proxyapi_base_url: str = "https://api.proxyapi.ru/openai/v1"
    database_path: str = "greenbuddy.db"


def get_settings() -> Settings:
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    proxyapi_key = os.getenv("PROXYAPI_KEY", "").strip()
    vision_model = os.getenv("VISION_MODEL", "gpt-4o-mini").strip()
    proxyapi_base_url = os.getenv("PROXYAPI_BASE_URL", "https://api.proxyapi.ru/openai/v1").strip()
    database_path = os.getenv("DATABASE_PATH", "greenbuddy.db").strip()

    if not telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is missing")
    if not proxyapi_key:
        raise RuntimeError("PROXYAPI_KEY is missing")

    return Settings(
        telegram_bot_token=telegram_bot_token,
        proxyapi_key=proxyapi_key,
        vision_model=vision_model,
        proxyapi_base_url=proxyapi_base_url,
        database_path=database_path,
    )
