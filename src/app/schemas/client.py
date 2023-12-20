from pydantic import BaseModel


class ClientBase(BaseModel):
    telegram_id: int

class ClientCreate(ClientBase):
    telegram_id: int

class ClientDB(ClientCreate):
    telegram_id: int

    class Config:
        """ORM config."""

        from_attributes = True
