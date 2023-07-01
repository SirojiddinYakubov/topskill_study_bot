from aiogram import Dispatcher, Bot

from bot.config import settings
from bot.handlers.user_handlers import UserHandler
from bot.handlers.main_handlers import MainHandler

bot = Bot(token=settings.TOKEN_API)
dp = Dispatcher(bot=bot)

user_handler = UserHandler(dp=dp, bot=bot)
main_handler = MainHandler(dp=dp, bot=bot)
