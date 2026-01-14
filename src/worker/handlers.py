from aio_pika import Message


async def on_message(msg: Message):
    async with msg.process():
        data = msg.body.decode()
        print(f"영상 분석: {data}")
