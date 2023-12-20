from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.ticket import ticket_crud


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
