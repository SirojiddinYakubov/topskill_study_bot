from aiogram import types

import crud.message_crud
from bot.config import settings
from bot.handlers.base_handler import BaseHandler
from bot.keyboards.user_keyboards import signup_ikb, redirect_to_hw_kb
from bot.schemas.message_schemas import GetMessageSchema
from crud import user_crud
from crud.user_crud import user_collection


class UserHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ Register user handlers """
        self.dp.register_message_handler(self.share_contact, content_types=types.ContentType.CONTACT)

    async def share_contact(self, message: types.Message):
        contact = message.contact

        error_msg = f"Siz ulashilgan telefon raqam bilan topskill platformasidan ro'yhatdan o'tmagansiz!\nIltimos avval {contact.phone_number} raqam orqali ro'yhatdan o'tib, ana shundan so'ng botni qayta ishga tushiring."

        obj = await user_collection.find_one({"_id": message.chat.id})
        if not obj:
            user = await user_crud.create_user(message.chat.id, contact.phone_number)
            if not user:
                return await message.answer(
                    text=error_msg,
                    reply_markup=signup_ikb())

            await self.bot.send_message(settings.ADMIN_ID, f"New user with phone {contact.phone_number} connected.")
        else:
            user = await user_crud.update_user(message.chat.id, contact.phone_number)
            if not user:
                return await message.answer(
                    text=error_msg,
                    reply_markup=signup_ikb()
                )
        await message.answer("Bot muvaffaqiyatli sozlandi. Endi biz sizga o'quv jarayoni haqida xabarlar yuboramiz 👍",
                             reply_markup=types.ReplyKeyboardRemove())

    async def create_message(self, payload: GetMessageSchema):
        obj = await user_collection.find_one({"user_id": str(payload.receiver_id)})
        if obj:
            await self.bot.send_message(obj['_id'], payload.content,
                                        reply_markup=redirect_to_hw_kb(status=payload.status,
                                                                       callback_url=payload.callback_url))

            await crud.message_crud.create_message(payload=payload)

            return {"status": "success", "message": "Message send successfully"}
        else:
            return {"status": "success", "message": "This user not found"}
