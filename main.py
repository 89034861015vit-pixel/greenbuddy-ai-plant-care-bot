from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from .config import get_settings
from .db import Database
from .vision import analyze_plant_photo
from .viz import create_health_chart

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()
bot = Bot(token=settings.telegram_bot_token)
dp = Dispatcher()
db = Database(settings.database_path)


@dp.message(Command("start"))
async def start(message: Message) -> None:
    await message.answer(
        "🌿 GreenBuddy is ready.\n\n"
        "Send me a plant photo and I will analyze its condition.\n"
        "Use /plant Ficus to set the current plant name.\n"
        "Use /stats to see health progress."
    )


@dp.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "Commands:\n"
        "/start — start the bot\n"
        "/plant NAME — set current plant name\n"
        "/stats — show plant health chart\n\n"
        "Then send a clear plant photo."
    )


@dp.message(Command("plant"))
async def set_plant(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    text = message.text or ""
    plant_name = text.replace("/plant", "", 1).strip()
    if not plant_name:
        await message.answer("Write it like this: /plant Ficus")
        return
    db.set_current_plant(user_id, plant_name)
    await message.answer(f"Current plant: {plant_name}")


@dp.message(Command("stats"))
async def stats(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    logs = db.get_logs(user_id, limit=20)
    if not logs:
        await message.answer("No plant logs yet. Send a plant photo first.")
        return
    chart_path = create_health_chart(logs)
    await message.answer_photo(FSInputFile(chart_path), caption="Plant health progress")


@dp.message(F.photo)
async def photo_handler(message: Message) -> None:
    user_id = message.from_user.id if message.from_user else 0
    plant_name = db.get_current_plant(user_id)

    await message.answer("Analyzing the plant photo...")

    try:
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)
        downloaded = await bot.download_file(file.file_path)
        if downloaded is None:
            await message.answer("I could not download the photo. Try again.")
            return

        image_bytes = downloaded.read()
        analysis = await analyze_plant_photo(
            image_bytes=image_bytes,
            api_key=settings.proxyapi_key,
            base_url=settings.proxyapi_base_url,
            model=settings.vision_model,
        )
        db.add_log(user_id, plant_name, analysis)

        answer = (
            f"🌿 Plant: {plant_name}\n"
            f"State: {analysis.get('plant_state', 'Unknown')}\n"
            f"Health score: {analysis.get('health_score', 50)}/100\n\n"
            f"Diagnosis: {analysis.get('diagnosis', 'No diagnosis')}\n\n"
            f"Next action: {analysis.get('care_action', 'Observe the plant and check soil moisture.')}\n\n"
            f"Watering: {analysis.get('watering', 'Check soil before watering.')}\n"
            f"Light: {analysis.get('light', 'Bright indirect light is usually safe.')}\n"
            f"Risk: {analysis.get('risk_level', 'medium')}"
        )
        await message.answer(answer)

    except Exception as error:
        logger.exception("Photo analysis failed")
        await message.answer(
            "Something went wrong during analysis. "
            "Check API key, model access, and try a clearer photo."
        )


@dp.message()
async def fallback(message: Message) -> None:
    await message.answer("Send a plant photo, or use /help.")


async def main() -> None:
    logger.info("GreenBuddy bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
