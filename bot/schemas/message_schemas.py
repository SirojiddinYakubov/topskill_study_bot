from uuid import UUID

from pydantic.main import BaseModel


class MessageSchema(BaseModel):
    sender_id: UUID
