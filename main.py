import logging
import os

import uvicorn
from aiogram import types, Dispatcher, Bot
from fastapi import FastAPI

from bot.config import settings
from bot.core import dp, bot, user_handler
from bot.schemas.message_schemas import GetMessageSchema

app = FastAPI()
WEBHOOK_PATH = "/study-bot/"
WEBHOOK_URL = settings.WEBHOOK_HOST + WEBHOOK_PATH


# https://api.telegram.org/bot{TOKEN_API}/getwebhookinfo

@app.on_event("startup")
async def on_startup():
    logging.warning('Start up server..')

    await bot.delete_webhook(drop_pending_updates=True)

    webhook_info = await bot.get_webhook_info()
    logging.info(webhook_info)
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


@app.post(f"{WEBHOOK_PATH}createMessage")
async def create_message(payload: GetMessageSchema):
    return await user_handler.create_message(payload)


@app.on_event("shutdown")
async def on_shutdown():
    logging.warning('Shutting down..')
    session = await bot.get_session()
    await session.close()


if __name__ == '__main__':
    try:
        uvicorn.run("__main__:app", host="0.0.0.0", port=8008, reload=True, workers=4, log_config='log.ini')
    except FileNotFoundError:
        os.mkdir('logs')
        open('logs/debug.log', 'a').close()
