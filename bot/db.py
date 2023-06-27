from motor import motor_asyncio
from dotenv import load_dotenv
import os

load_dotenv(".env")

# Database
MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_HOST = os.getenv("MONGODB_HOST")
MONGODB_PORT = os.getenv("MONGODB_PORT")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

cluster = motor_asyncio.AsyncIOMotorClient(
    "mongodb://{user}:{password}@{host}:{port}/{database}?retryWrites=true&w=majority".format(
        user=MONGODB_USER,
        password=MONGODB_PASSWORD,
        host=MONGODB_HOST,
        port=MONGODB_PORT,
        database=MONGODB_DATABASE
    )
)

# COLLECTION_NAME = 'topskill_study_collection'

database = cluster[MONGODB_DATABASE]
# collections = database[COLLECTION_NAME]
