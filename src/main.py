from dotenv import load_dotenv
load_dotenv(override=True)

import asyncio
import signal
from functools import partial

from infra.rabbitmq_client import RabbitMQClient
from worker.handlers import on_message
from config.constants import RabbitMQConfig


async def main():
    shutdown_event = asyncio.Event()

    def signal_handler(*_):
        shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    async with RabbitMQClient() as rabbitmq:
        await rabbitmq.consume(
            RabbitMQConfig.VIDEO_PROCESS,
            partial(on_message, rabbitmq=rabbitmq)
        )
        await shutdown_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
