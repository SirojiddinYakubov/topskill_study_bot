import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

import aiohttp

from bot.config import settings
from bot.db import database

COLLECTION_NAME = 'users'

print(13, database)

user_collection = database[COLLECTION_NAME]
print(16, user_collection)

# async def get_access_token() -> str:
#     auth_url = "https://topskill.uz/api/v1/site/auth/jwt/login"
#     data = {
#         "username": settings.TOPSKILL_LOGIN,
#         "password": settings.TOPSKILL_PASSWORD,
#     }
#     access_token = ""
#     async with aiohttp.ClientSession(trust_env=True) as client:
#         async with client.post(auth_url, data=data, ssl=False) as resp:
#             if resp.status == 200:
#                 resp_data = await resp.json()
#                 access_token = resp_data['access_token']
#     return access_token


async def get_user_id(phone: str) -> Optional[UUID]:
    url = f"{settings.BACK_BASE_URL}/api/v1/site/users/get-id-by-phone?phone={phone}"
    async with aiohttp.ClientSession(trust_env=True) as client:
        async with client.get(url, ssl=False) as resp:
            if resp.status == 200:
                resp_data = await resp.json()
                return resp_data
            else:
                logging.error(f"User not found with phone {phone}")


# print(asyncio.run(get_user_id("998919791999")))
# asyncio.run(get_access_token())


async def create_user(_id: int, phone_number: str):
    logging.info(f"Inside create_user: _id: {_id}, phone_number: {phone_number}")
    user_id = await get_user_id(phone_number)

    if not user_id:
        return None

    return await user_collection.insert_one({
        "_id": _id,
        "user_id": user_id,
        "created_at": str(datetime.now()),
        "updated_at": None,
        "phone": phone_number,
        "status": "active",
        "lang": "uz"
    })


async def update_user(_id: int, phone_number: str):
    logging.info(f"Inside update_user: _id: {_id}, phone_number: {phone_number}")
    user_id = await get_user_id(phone_number)

    if not user_id:
        return None

    result = await user_collection.update_one({"_id": _id}, {"$set": {
        "updated_at": str(datetime.now()),
        "phone": phone_number,
        "user_id": user_id,
    }})

    # print('updated %s document' % result)
    # new_document = await user_collection.find_one({'_id': _id})
    # print('document is now %s' % new_document)
    return result



