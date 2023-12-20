import json

import aio_pika


async def connect_to_broker(
        channel,
        exchange_name,
        routing_key,
        queue_name,
        message_body,
):
    async with channel:
        exchange = await channel.declare_exchange(
            exchange_name, type='direct', durable=True, auto_delete=False,
        )

        queue = await channel.declare_queue(queue_name, durable=True)

        await queue.bind(exchange, routing_key)

        await exchange.publish(
            aio_pika.Message(body=message_body.encode()),
            routing_key=routing_key,
        )


async def change_status(ticket, broker):
    channel = broker.get_channel()
    exchange_name = 'change_status'
    routing_key = 'message_queue'
    queue_name = 'message_queue'
    message_body = json.dumps({
        'message': f'Статус сообщения изменен:\n<b>{ticket.status.value}</b>',
        'telegram_id': 222160065,
    })

    connect_to_broker(
        channel,
        exchange_name,
        routing_key,
        queue_name,
        message_body,
    )


async def send_message_from_employee(message, broker):
    channel = broker.get_channel()
    exchange_name = 'send_message'
    routing_key = 'message_queue'
    queue_name = 'message_queue'
    message_body = json.dumps({
        'message': f'{message}',
        'telegram_id': 222160065,
    })

    connect_to_broker(
        channel,
        exchange_name,
        routing_key,
        queue_name,
        message_body,
    )
