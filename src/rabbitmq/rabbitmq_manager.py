from aio_pika import connect_robust, RobustConnection, RobustChannel, Message, DeliveryMode
from fsspec import Callback

from config.constants import Messages, RabbitMQConfig
from config.env import get_config

config = get_config()


class RabbitMQManager:
    def __init__(self):
        self.connection: RobustConnection | None = None
        self.channel: RobustChannel | None = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def connect(self):
        if self.connection is not None:
            return

        self.connection = await connect_robust(
            config.rabbitmq.host,
            heartbeat=config.rabbitmq.heart_beat,
        )

        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

        await self.channel.declare_queue(
            RabbitMQConfig.VIDEO_PROCESS,
            durable=True,
        )
        await self.channel.declare_queue(
            RabbitMQConfig.VIDEO_RESULT,
            durable=True,
        )

    async def consume(self, queue_name: str, callback: Callback):
        if self.channel is None:
            raise RuntimeError(Messages.Error.RABBITMQ_NOT_INIT)

        queue = await self.channel.get_queue(queue_name)
        await queue.consume(callback)

    async def publish(self, message: str, routing_key: str):
        if self.channel is None:
            raise RuntimeError(Messages.Error.RABBITMQ_NOT_INIT)

        await self.channel.default_exchange.publish(
            Message(body=message.encode(), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=routing_key
        )

    async def close(self):
        if self.channel:
            await self.channel.close()
            self.channel = None
        if self.connection:
            await self.connection.close()
            self.connection = None
