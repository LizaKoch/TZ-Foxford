import asyncio
import json
import logging
import sys
from os import getenv
from functools import partial

import aiohttp
from aiogram import Bot, Dispatcher, F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters.command import CommandStart
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv

import aio_pika

from config import settings

load_dotenv('.env')
BOT_TOKEN = getenv('BOT_TOKEN')

form_router = Router()


class CreateTicket(StatesGroup):
    name = State()
    CreateTicket = State()


@form_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        'Привет! Пиши и мы свяжемся с тобой.',
    )
    async with aiohttp.ClientSession() as session:
        async with session.post(
                settings.api_client,
                json={'telegram_id': message.from_user.id},
        ) as resp:
            logging.info(resp)



@form_router.message(F.text)
async def create_message(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                settings.api_message,
                json={'telegram_id': message.from_user.id, 'message': message.text},
        ) as resp:
            if resp.status == 200:
                return await message.answer('С вами свяжутся в ближайшее время')


async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
    bot: Bot
) -> None:
    async with message.process():
        data = json.loads(message.body)
        await bot.send_message(data['telegram_id'], data['message'])
        await asyncio.sleep(0.1)

async def run_pika(bot):
    connection = await aio_pika.connect_robust(
        f"amqp://developer:1q2w3e4r@127.0.0.1/",
    )

    process_message_with_bot = partial(process_message, bot=bot)

    queue_name = "test_queue"

    # Creating channel
    channel = await connection.channel()

    # Maximum message count which will be processing at the same time.
    await channel.set_qos(prefetch_count=100)

    # Declaring queue
    queue = await channel.declare_queue(queue_name, durable=True)

    await queue.consume(process_message_with_bot)

    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await connection.close()



async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(form_router)

    await asyncio.gather(
        dp.start_polling(bot),
        run_pika(bot),
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
