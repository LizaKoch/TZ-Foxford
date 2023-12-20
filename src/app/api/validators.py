from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.ticket import ticket_crud
from src.app.models.ticket import TicketStatus


async def check_previous_ticket_closed(
        telegram_id: int,
        session: AsyncSession,
):
    """Check if the previous ticket is closed."""
    ticket = await ticket_crud.get_open_ticket_by_user(
        telegram_id=telegram_id,
        session=session,
    )
    if ticket:
        return ticket
    return None


async def check_ticket_is_exist(
        ticket_id: int,
        session: AsyncSession,
):
    """Check if the ticket exists."""
    ticket = await ticket_crud.get(
        obj_id=ticket_id,
        session=session,
    )
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Тикет не найден!',
        )

async def check_ticket_already_closed(
        ticket_id: int,
        session: AsyncSession,
):
    """Check if the ticket is already closed."""
    ticket = await ticket_crud.get(
        obj_id=ticket_id,
        session=session,
    )
    if ticket.status == TicketStatus.CLOSED:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Тикет уже закрыт!',
        )

async def check_the_same_ticket_status(
        ticket_id: int,
        ticket_status: str,
        session: AsyncSession,
):
    """Check if the ticket status is the same."""
    ticket = await ticket_crud.get(
        obj_id=ticket_id,
        session=session,
    )
    if ticket.status == ticket_status:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Статус тикета не изменился!',
        )
