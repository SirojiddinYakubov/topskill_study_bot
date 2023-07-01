import pathlib
from typing import Optional, Any, Union

from pydantic.class_validators import validator
from pydantic.env_settings import BaseSettings

BASE_DIR = pathlib.Path(__file__).parents[1]


class Settings(BaseSettings):
    BOT_API: str
    BOT_HASH: str

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
    TOPSKILL_LOGIN: str
    TOPSKILL_PASSWORD: str

    class Config:
        env_file = ".env"


settings = Settings()
