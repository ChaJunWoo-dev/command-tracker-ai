from dotenv import load_dotenv
load_dotenv(override=True)

import asyncio
import signal

from rabbitmq.rabbitmq_manager import RabbitMQManager
from temp_callback import on_message
from config.constants import RabbitMQConfig

async def main():
    shutdown_event = asyncio.Event()

    def signal_handler(*_):
        shutdown_event.set()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    async with RabbitMQManager() as rabbitmq:
        await rabbitmq.consume(RabbitMQConfig.VIDEO_PROCESS, on_message)
        await shutdown_event.wait()

if __name__ == "__main__":
    asyncio.run(main())
