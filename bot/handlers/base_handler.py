from aiogram import Dispatcher, Bot
from motor.motor_asyncio import AsyncIOMotorCollection


class BaseHandler:
    def __init__(self, dp: Dispatcher, bot: Bot, collection: AsyncIOMotorCollection = None):
        self.dp = dp
        self.bot = bot
        self.collection = collection
