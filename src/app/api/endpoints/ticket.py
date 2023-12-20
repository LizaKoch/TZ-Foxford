from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.validators import (
    check_the_same_ticket_status,
    check_ticket_already_closed,
    check_ticket_is_exist,
)
from src.app.core.db import get_async_session
from src.app.core.publisher import change_status
from src.app.core.rabbit import MessageBroker, get_message_broker
from src.app.core.user import User, current_auth_user
from src.app.crud.ticket import ticket_crud
from src.app.schemas.ticket import TicketDB, TicketFilter, TicketUpdate

router = APIRouter(
    prefix='/tickets',
    tags=['Tickets'],
)

@router.get(
    '/',
    response_model=list[TicketDB],
    response_model_exclude_none=True,
)
async def get_all_tickets(
    session: AsyncSession = Depends(get_async_session),
    ticket_filter: TicketFilter = FilterDepends(TicketFilter),
    user: User = Depends(current_auth_user),
):
    """Get all tickets."""
    return await ticket_crud.get_multi_with_filter(session, ticket_filter)


@router.patch(
    '/{ticket_id}',
    response_model=TicketDB,
    response_model_exclude_none=True,
)
async def update_ticket(
    ticket_id: int,
    ticket: TicketUpdate,
    session: AsyncSession = Depends(get_async_session),
    broker: MessageBroker = Depends(get_message_broker),
    user: User = Depends(current_auth_user),
):
    """Update status of ticket."""
    await check_ticket_is_exist(ticket_id=ticket_id, session=session)
    await check_ticket_already_closed(ticket_id=ticket_id, session=session)
    await check_the_same_ticket_status(
        ticket_id=ticket_id,
        ticket_status=ticket.status,
        session=session)

    db_ticket = await ticket_crud.get(obj_id=ticket_id, session=session)

    await change_status(ticket=ticket, broker=broker)

    return await ticket_crud.update(db_ticket, ticket, session)
