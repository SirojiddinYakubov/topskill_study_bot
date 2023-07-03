import redis

from bot.config import settings


def get_redis_client() -> redis.Redis:
    redis_client = redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    return redis_client
