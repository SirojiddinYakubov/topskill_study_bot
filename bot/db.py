from motor import motor_asyncio

from bot.config import settings

cluster = motor_asyncio.AsyncIOMotorClient(
    "mongodb://{user}:{password}@{host}:{port}/{database}?retryWrites=true&w=majority".format(
        user=settings.MONGODB_USER,
        password=settings.MONGODB_PASSWORD,
        host=settings.MONGODB_HOST,
        port=settings.MONGODB_PORT,
        database=settings.MONGODB_DATABASE
    )
)

# COLLECTION_NAME = 'topskill_study_collection'

database = cluster[settings.MONGODB_DATABASE]
# collections = database[COLLECTION_NAME]
