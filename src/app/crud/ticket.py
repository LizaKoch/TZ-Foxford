from typing import Optional, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.db import Base
from src.app.crud.base import CRUDBase
from src.app.models.client import Client
from src.app.models.ticket import Ticket
from src.app.models.user import User
from src.app.schemas.ticket import TicketCreate, TicketFilter, TicketUpdate

ModelType = TypeVar('ModelType', bound=Base)


class TicketCRUD(CRUDBase[Ticket, TicketCreate, TicketUpdate]):
    async def get_multi_with_filter(
        self,
        session: AsyncSession,
        filters: TicketFilter,
    ) -> list[Ticket]:
        if filters.status:
            query = select(Ticket).where(
                self.model.status == filters.status,
            )
        if filters.employee_id:
            query = select(Ticket).where(
                self.model.employee_id == filters.employee_id,
            )
        if filters.created_at:
            filters.created_at = filters.created_at.strftime('%Y-%m-%d')
            query = select(Ticket).where(
                func.date(
                    self.model.created_at,
                )
                == func.date(filters.created_at),
            )
        if filters.updated_at:
            filters.updated_at = filters.updated_at.strftime('%Y-%m-%d')
            query = select(Ticket).where(
                func.date(
                    self.model.updated_at,
                )
                == func.date(filters.updated_at),
            )
        else:
            query = select(Ticket)
        result = await session.execute(query)
        return result.scalars().all()

    async def get_open_ticket_by_user(
        self,
        telegram_id: int,
        session: AsyncSession,
    ) -> Optional[Ticket]:
        client_id = await self.get_client_id_by_telegram_id(
            telegram_id=telegram_id,
            session=session,
        )
        ticket_db = await session.execute(
            select(Ticket).where(
                Ticket.client_id == client_id,
                ((Ticket.status == 'OPEN') |
                (Ticket.status == 'IN_PROGRESS')),
            ),
        )
        return ticket_db.scalars().first()

    async def get_client_id_by_telegram_id(
        self,
        telegram_id: int,
        session: AsyncSession,
    ) -> Optional[int]:
        client_id = await session.execute(
            select(Client.id).where(Client.telegram_id == telegram_id),
        )
        return client_id.scalars().first()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
    ) -> ModelType:
        obj_in_data = obj_in.dict()

        if user is not None:
            obj_in_data['user_id'] = user.id
        client_id = await self.get_client_id_by_telegram_id(
            telegram_id=obj_in_data.pop('telegram_id'),
            session=session,
        )
        db_object = self.model(client_id=client_id)

        session.add(db_object)
        await session.commit()
        await session.refresh(db_object)
        return db_object


ticket_crud = TicketCRUD(Ticket)
