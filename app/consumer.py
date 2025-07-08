import json

import aio_pika.abc

from app.infrastructure.broker.accessor import get_broker_connection


async def make_amqp_consumer():
    connection = await get_broker_connection()
    channel = await connection.channel()
    queue = await channel.declare_queue('callback_queue', durable=True)
    await queue.consume(consume_callback)


async def consume_callback(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        body = json.loads(message.body.decode())
        correlation_id = message.correlation_id
        print(body, correlation_id)
