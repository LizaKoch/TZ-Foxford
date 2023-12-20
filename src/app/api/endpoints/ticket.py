import json
import aio_pika

from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.validators import check_ticket_is_exist
from src.app.core.db import get_async_session
from src.app.crud.ticket import ticket_crud
from src.app.schemas.ticket import TicketDB, TicketFilter, TicketUpdate
from src.app.core.rabbit import MessageBroker, get_message_broker

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
):
    """Update ticket."""
    await check_ticket_is_exist(ticket_id, session)
    db_ticket = await ticket_crud.get(obj_id=ticket_id, session=session)

    # channel = broker.get_channel()
    # exchange_name = "test_excange"
    # routing_key = "test_queue"
    # message_body = json.dumps({
    #     "message": "Ответ от службы поддержки: \n <i>its work!!!</i>",
    #     "telegram_id": 222160065
    # })
    #
    # # Асинхронная операция объявления обмена с автоматическим созданием, если он не существует
    # async with channel:
    #     exchange = await channel.declare_exchange(
    #         exchange_name, type="direct", durable=True, auto_delete=False
    #     )
    #
    #     # Отправка сообщения
    #     await exchange.publish(
    #         aio_pika.Message(body=message_body.encode()),
    #         routing_key=routing_key
    #     )

    channel = broker.get_channel()
    exchange_name = "your_exchange_name"
    routing_key = "your_routing_key"
    queue_name = "test_queue"
    message_body = json.dumps({
        "message": f"Статус сообщения изменен:\n<b>{ticket.status.value}</b>",
        "telegram_id": 222160065
    })

    # Асинхронная операция объявления обмена с автоматическим созданием, если он не существует
    async with channel:
        exchange = await channel.declare_exchange(
            exchange_name, type="direct", durable=True, auto_delete=False
        )

        # Опционально, объявление очереди
        queue = await channel.declare_queue(queue_name, durable=True)

        # Привязка очереди к обмену
        await queue.bind(exchange, routing_key)

        # Отправка сообщения на обмен, которое будет автоматически маршрутизировано в очередь
        await exchange.publish(
            aio_pika.Message(body=message_body.encode()),
            routing_key=routing_key
        )

    return await ticket_crud.update(db_ticket, ticket, session)
