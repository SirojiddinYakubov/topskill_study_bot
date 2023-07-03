import pathlib
from typing import Optional, Any, Union

from pydantic.class_validators import validator
from pydantic.env_settings import BaseSettings
from pydantic.networks import AnyHttpUrl

BASE_DIR = pathlib.Path(__file__).parents[1]


class Settings(BaseSettings):
    BOT_API: str
    BOT_HASH: str

    FRONT_BASE_URL: Optional[AnyHttpUrl] = "https://topskill.uz"
    BACK_BASE_URL: Optional[AnyHttpUrl] = "https://topskill.uz"
    WEBHOOK_HOST: Optional[AnyHttpUrl] = "http://134.209.104.18:8008"

    TOKEN_API: Optional[str]

    @validator("TOKEN_API", pre=True, allow_reuse=True)
    def assemble_token_api(cls, v: Optional[str], values: dict[str, Any]) -> str:
        return f"{values.get('BOT_API')}:{values.get('BOT_HASH')}"

    REDIS_HOST: str
    REDIS_PORT: Union[str, int]

    MONGODB_USER: str
    MONGODB_PASSWORD: str
    MONGODB_HOST: str
    MONGODB_PORT: Union[str, int]
    MONGODB_DATABASE: str

    ADMIN_ID: Union[str, int]

    class Config:
        env_file = ".env"


settings = Settings()
