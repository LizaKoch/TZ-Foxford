from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator


class Message(BaseModel):
    ticket_id: int
    employee_id: Optional[int] = None
    text: str

class MessageCreate(BaseModel):
    text: str
    telegram_id: Optional[int] = None
    ticket_id: Optional[int] = None
    @model_validator(mode='before')
    @classmethod
    def check_telegram_id_or_ticket_id(cls, values: any):
        if (values.get('telegram_id') is None) and (values.get('ticket_id') is None):  # noqa: E501
            raise ValueError('either telegram_id or ticket_id is required')
        return values

class MessageDB(BaseModel):
    ticket_id: int
    employee_id: Optional[int] = None
    text: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        """ORM config."""

        from_attributes = True
