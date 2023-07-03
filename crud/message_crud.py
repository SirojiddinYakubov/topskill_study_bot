import logging

from bot.db import database
from bot.schemas.message_schemas import GetMessageSchema

COLLECTION_NAME = 'messages'

message_collection = database[COLLECTION_NAME]


async def create_message(payload: GetMessageSchema):
    logging.info(f"Inside create_message: {payload.dict()}")

    return await message_collection.insert_one({
        "sender_id": str(payload.sender_id),
        "receiver_id": str(payload.receiver_id),
        "content": payload.content,
        "status": str(payload.status),
        "callback_url": payload.callback_url
    })
