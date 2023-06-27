from aiogram import types, Dispatcher

from bot.keyboards.user_keyboards import get_main_kb, get_contact_kb, get_start_kb, signup_ikb
from crud import user_crud
from crud.user_crud import user_collection
from aiogram import Bot


async def start_command(message: types.Message):
    user = await user_collection.find_one({"_id": message.chat.id})

    text = "Assalomu aleykum. Topskill o'quv platformasining botiga xush kelibsiz!"
    if not (message.contact or user):
        text += "\n\nPlatforma bilan aloqani yo'lga qo'yish uchun iltimos telefon raqamingizni jo'nating!"
        await message.answer(text=text, reply_markup=get_contact_kb())
    else:
        await message.answer(text=text, reply_markup=get_main_kb())


async def share_contact(message: types.Message):
    contact = message.contact

    obj = await user_collection.find_one({"_id": message.chat.id})
    if not obj:
        user = await user_crud.create_user(message.chat.id, contact.phone_number)
        if not user:
            return await message.answer(
                text="Siz topskill platformasidan ro'yhatdan o'tmagansiz!\n"
                     "Iltimos avval ro'yhatdan o'tib botni qayta ishga tushiring.",
                reply_markup=signup_ikb())
    else:
        await user_crud.update_user(message.chat.id, contact.phone_number)
    await message.answer("Endi biz sizga o'quv jarayoni haqida xabarlar yuboramiz 👍",
                         reply_markup=types.ReplyKeyboardRemove())


def register_user_handler(dp: Dispatcher, bot: Bot) -> None:
    """ Register user handlers """
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(share_contact, content_types=types.ContentType.CONTACT)
