import os
import pathlib

from aiogram import Dispatcher, Bot

from bot.handlers.user_handlers import register_user_handler

BASE_DIR = pathlib.Path(__file__).parents[1]

TOKEN_API = f"{os.getenv('BOT_API')}:{os.getenv('BOT_HASH')}"
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot=bot)


def register_handler(dp: Dispatcher, bot: Bot) -> None:
    register_user_handler(dp, bot)


register_handler(dp=dp, bot=bot)
