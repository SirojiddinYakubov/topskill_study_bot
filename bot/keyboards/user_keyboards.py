from aiogram import types


def get_main_kb() -> types.ReplyKeyboardMarkup:
    """
        Get ikb for menu
    :return:
    """
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("Button 1"))


def get_start_kb() -> types.ReplyKeyboardMarkup:
    """
        Get ikb for menu
    :return:
    """
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton("/start"))


def signup_ikb() -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Ro'yhatdan o'tish", url="https://topskill.uz/auth/signup")]
    ])


def get_contact_kb() -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        types.KeyboardButton("Telefon raqamni ulashish 📲", request_contact=True)
    )

# , one_time_keyboard=True
