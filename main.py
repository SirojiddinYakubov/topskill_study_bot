import logging

import uvicorn
from aiogram import types, Dispatcher, Bot
from fastapi import FastAPI

from bot.config import settings
from bot.main import dp, bot, user_handler
from bot.schemas.message_schemas import MessageSchema

app = FastAPI()
WEBHOOK_PATH = f"/bot/{settings.TOKEN_API}"
WEBHOOK_URL = "https://db13-195-158-30-67.ngrok-free.app" + WEBHOOK_PATH


# https://api.telegram.org/bot776249055:AAH_Zce3av-IfdDLdscVpapdz6g-ksbtdsrg/getwebhookinfo

@app.on_event("startup")
async def on_startup():
    logging.warning('Start up server..')

    await bot.delete_webhook(drop_pending_updates=True)

    webhook_info = await bot.get_webhook_info()
    print(webhook_info)
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    logging.debug(f"Update from telegram: {update}")
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


@app.post(f"{WEBHOOK_PATH}/createMessage")
async def create_message(payload: MessageSchema):
    return await user_handler.create_message(payload)


@app.on_event("shutdown")
async def on_shutdown():
    logging.warning('Shutting down..')
    session = await bot.get_session()
    await session.close()


if __name__ == '__main__':
    uvicorn.run("__main__:app", host="0.0.0.0", port=8080, reload=True, workers=4, log_config='log.ini')
