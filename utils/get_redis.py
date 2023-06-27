import redis

from bot.config import REDIS_HOST, REDIS_PORT


def get_redis_client() -> redis.Redis:
    redis_client = redis.from_url(
        f"redis://{REDIS_HOST}:{REDIS_PORT}",
        max_connections=10,
        encoding="utf8",
        decode_responses=True,
    )
    return redis_client
