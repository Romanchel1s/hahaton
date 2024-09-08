import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from bot.config import TOKEN, API_URL
import httpx


async def send_post_request(data: dict) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=data)
        response.raise_for_status()
        return response.json()

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        data = {
            # "user_id": message.from_user.id,
            "query": message.text,
        }

        response = await send_post_request(data)
        
        result_text = response.get("text", "Ответ не получен.")

        await message.answer(f"Результат запроса: {result_text}")

    except httpx.HTTPStatusError as e:
        await message.answer(f"Произошла ошибка при запросе: {str(e)}")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())