import enum
from uuid import UUID

from pydantic.main import BaseModel
from pydantic.networks import AnyHttpUrl


class HomeworkStatusEnum(str, enum.Enum):
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    WAITING = 'waiting'


class GetMessageSchema(BaseModel):
    sender_id: UUID
    receiver_id: UUID
    content: str
    status: HomeworkStatusEnum
    callback_url: AnyHttpUrl
