import logging
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
from bot.config import dp, bot, TOKEN_API

load_dotenv('.env')

app = FastAPI()
WEBHOOK_PATH = f"/bot/{TOKEN_API}"
WEBHOOK_URL = "https://f223-195-158-30-67.ngrok-free.app" + WEBHOOK_PATH


# https://api.telegram.org/bot776249055:AAH_Zce3av-IfdDLdscVpapdz6g-ksbtSHw/getwebhookinfo

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


@app.on_event("shutdown")
async def on_shutdown():
    logging.warning('Shutting down..')
    session = await bot.get_session()
    await session.close()


if __name__ == '__main__':
    uvicorn.run("__main__:app", host="0.0.0.0", port=8080, reload=True, workers=4, log_config='log.ini')
