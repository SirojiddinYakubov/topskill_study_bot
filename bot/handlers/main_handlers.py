from aiogram import types

from bot.handlers.base_handler import BaseHandler
from bot.keyboards.user_keyboards import get_contact_kb
from crud.user_crud import user_collection


class MainHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Register main handlers """
        self.dp.register_message_handler(self.start_command, commands=['start'])

    async def start_command(self, message: types.Message):
        user = await user_collection.find_one({"_id": message.chat.id})

        text = "Assalomu aleykum. Topskill o'quv platformasining botiga xush kelibsiz!"
        if not (message.contact or user):
            text += "\n\nPlatforma bilan aloqani yo'lga qo'yish uchun iltimos telefon raqamingizni ulashing!"
            await message.answer(text=text, reply_markup=get_contact_kb())
        else:
            await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
