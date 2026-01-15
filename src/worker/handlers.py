import json
from aio_pika import IncomingMessage

from infra.s3_client import S3Client
from infra.ffmpeg_client import FFmpegClient
from infra.rabbitmq_client import RabbitMQClient
from infra.temp_storage import TempStorage
from config.settings import get_config
from config.constants import RabbitMQConfig, Messages

config = get_config()


async def on_message(msg: IncomingMessage, rabbitmq: RabbitMQClient):
    async with msg.process():
        data = json.loads(msg.body.decode())

        job_id = data["key"]
        original_s3_key = f"original/{data['key']}"
        start = data["trimStart"]
        end = data["trimEnd"]

        storage = TempStorage()
        ffmpeg = FFmpegClient()

        async with S3Client() as s3, storage.job_dir(job_id) as job:
            ext = original_s3_key.split(".")[-1]
            input_path = job / f"raw.{ext}"
            output_path = job / f"cut.{ext}"
            processed_s3_key = f"processed/{data['key']}"

            try:
                await s3.download_file(original_s3_key, str(input_path), config.aws.bucket_name)
            except Exception as e:
                email = data["email"]
                message = { "email": email, "subject": Messages.Error.FAILED_DOWNLOAD }
                await rabbitmq.publish(message, RabbitMQConfig.VIDEO_RESULT)
                return

            try:
                await ffmpeg.cut(input_path, output_path, start, end)
            except Exception as e:
                email = data["email"]
                message = { "email": email, "subject": Messages.Error.FAILED_CUT }
                await rabbitmq.publish(message, RabbitMQConfig.VIDEO_RESULT)
                return

            # todo: AI분석
            # todo: 매핑
            # todo: 자막 삽입(편집)
            # todo: 결과물 전송(rabbitmq)

            # try:
            #     await s3.upload_file(str(output_path), processed_s3_key, config.aws.bucket_name)
            # except Exception as e:
            #     email = data["email"]
            #     message = { "email": email, "subject": Messages.Error.FAILED_UPLOAD }
            #     await rabbitmq.publish(message, RabbitMQConfig.VIDEO_RESULT)
            #     return
