
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.validators import check_previous_ticket_closed
from src.app.core.db import get_async_session
from src.app.core.publisher import send_message_from_employee
from src.app.core.rabbit import MessageBroker, get_message_broker
from src.app.core.user import User, current_user
from src.app.crud.message import message_crud
from src.app.crud.ticket import ticket_crud
from src.app.schemas.message import MessageCreate, MessageDB

router = APIRouter(
    prefix='/messages',
    tags=['Messages'],
)

@router.get(
    '/',
    response_model=list[MessageDB],
    response_model_exclude_none=True,
)
async def get_all_tickets(
    ticket_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Get all messages by ticket id."""
    return await message_crud.get_message_by_ticket_id(
        ticket_id=ticket_id,
        session=session,
    )


@router.post(
    '/',
    response_model=MessageDB,
    response_model_exclude_none=True,
)
async def create_message(
    request: MessageCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
    broker: MessageBroker = Depends(get_message_broker),
):
    """Create a new ticket."""
    ticket_id = request.ticket_id
    if request.telegram_id:
        ticket = await check_previous_ticket_closed(
            request.telegram_id,
            session,
        )
        if not ticket:
            ticket = await ticket_crud.create(request, session)
        ticket_id = ticket.id
    my_message = dict(text=request.text, ticket_id=ticket_id)
    message =  await message_crud.create(
        my_message,
        user=user,
        session=session,
    )
    if user:
        await send_message_from_employee(request.text, broker)
    return message
