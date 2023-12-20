from typing import Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db import Base
from src.app.crud.base import CRUDBase
from src.app.models.message import Message
from src.app.models.user import User
from src.app.schemas.message import MessageCreate

ModelType = TypeVar('ModelType', bound=Base)

class MessageCRUD(CRUDBase[Message, MessageCreate, None]):
    async def get_message_by_ticket_id(
            self,
            ticket_id: int,
            session: AsyncSession,
    ) -> Optional[list[Message]]:
        message_db = await session.execute(
            select(Message).where(Message.ticket_id == ticket_id),
        )
        return message_db.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None,
    ) -> ModelType:
        obj_in_data = obj_in

        if user is not None:
            obj_in_data['employee_id'] = user.id

        db_object = self.model(**obj_in_data)

        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object

message_crud = MessageCRUD(Message)
