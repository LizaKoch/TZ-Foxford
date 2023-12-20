import asyncio
import json

import aio_pika
from aiogram import Bot


async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
    bot: Bot,
) -> None:
    async with message.process():
        data = json.loads(message.body)
        await bot.send_message(data['telegram_id'], data['message'])
        await asyncio.sleep(0.1)
