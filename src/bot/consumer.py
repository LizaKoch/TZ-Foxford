from aiogram import Bot
import aio_pika
import asyncio


async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
    bot: Bot
) -> None:
    async with message.process():
        data = json.loads(message.body)
        await bot.send_message(data['telegram_id'], data['message'])
        await asyncio.sleep(0.1)

