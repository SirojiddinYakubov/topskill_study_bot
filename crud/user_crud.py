import logging
from datetime import datetime
from typing import Optional
from uuid import UUID

import aiohttp

from bot.config import settings
from bot.db import database

COLLECTION_NAME = 'users'

user_collection = database[COLLECTION_NAME]


async def get_access_token() -> str:
    auth_url = "https://topskill.uz/api/v1/site/auth/jwt/login"
    data = {
        "username": settings.TOPSKILL_LOGIN,
        "password": settings.TOPSKILL_PASSWORD,
    }
    access_token = ""
    async with aiohttp.ClientSession(trust_env=True) as client:
        async with client.post(auth_url, data=data, ssl=False) as resp:
            if resp.status == 200:
                resp_data = await resp.json()
                access_token = resp_data['access_token']
    return access_token


async def get_user_id(phone: str) -> Optional[UUID]:
    access_token = await get_access_token()
    me_url = f"https://topskill.uz/api/v1/admin/users/list/?q={phone}"
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + access_token
    }
    results = []
    async with aiohttp.ClientSession(trust_env=True) as client:
        async with client.get(me_url, ssl=False, headers=headers) as resp:
            if resp.status == 200:
                resp_data = await resp.json()
                if 'total_results' in resp_data and resp_data['total_results'] > 0:
                    results = resp_data['results']

    results = list(filter(lambda d: d['phone'] == phone, results))

    if len(results) == 1:
        return results[0]['id']


# print(asyncio.run(get_user_id("998919791999")))


# asyncio.run(get_access_token())


async def create_user(_id: int, phone_number: str):
    logging.info(f"Create user: _id: {_id}, phone_number: {phone_number}")
    created_at = datetime.now()
    user_id = await get_user_id(phone_number)

    if not user_id:
        return None

    return await user_collection.insert_one({
        "_id": _id,
        "user_id": user_id,
        "created_at": str(created_at),
        "updated_at": None,
        "phone": phone_number,
        "status": "active",
        "lang": "uz"
    })


async def update_user(_id: int, phone_number: str):
    logging.info(f"Update user: _id: {_id}, phone_number: {phone_number}")
    updated_at = datetime.now()

    user_id = await get_user_id(phone_number)

    if not user_id:
        return None

    result = await user_collection.update_one({"_id": _id}, {"$set": {
        "updated_at": str(updated_at),
        "phone": phone_number,
        "user_id": user_id,
    }})

    # print('updated %s document' % result)
    # new_document = await user_collection.find_one({'_id': _id})
    # print('document is now %s' % new_document)
    return result
