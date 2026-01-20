import json
from aio_pika import IncomingMessage

from infra.s3_client import S3Client
from infra.ffmpeg_client import FFmpegClient
from infra.rabbitmq_client import RabbitMQClient
from infra.temp_storage import TempStorage
from ai.detector import PersonDetector
from ai.pose_estimator import PoseEstimator
from services.video_analyzer import VideoAnalyzer
from config.settings import get_config
from config.constants import RabbitMQConfig, S3Config, ErrorCode, Messages
from config.exceptions import AppError

config = get_config()


async def on_message(
    msg: IncomingMessage,
    rabbitmq: RabbitMQClient,
    detector: PersonDetector,
    pose_estimator: PoseEstimator
):
    async with msg.process():
        data = json.loads(msg.body.decode())

        file_name = data["filename"]
        file_name_split = file_name.split(".")
        job_id = file_name_split[0]
        start = data["trimStart"]
        end = data["trimEnd"]

        storage = TempStorage()
        ffmpeg = FFmpegClient()

        async with S3Client() as s3, storage.job_dir(job_id) as job:
            ext = file_name_split[-1]
            input_path = job / f"raw.{ext}"
            output_path = job / f"cut.{ext}"
            final_path = job / f"final.{ext}"
            original_s3_key = f"{S3Config.ORIGINAL_PREFIX}/{file_name}"
            processed_s3_key = f"{S3Config.PROCESSED_PREFIX}/{file_name}"

            try:
                try:
                    await s3.download_file(original_s3_key, str(input_path), config.aws.bucket_name)
                except Exception as e:
                    raise AppError(ErrorCode.DOWNLOAD_FAILED, Messages.Error.DOWNLOAD_FAILED)

                try:
                    await ffmpeg.cut(input_path, output_path, start, end)
                except Exception as e:
                    raise AppError(ErrorCode.CUT_FAILED, Messages.Error.CUT_FAILED)

                try:
                    character = data["character"]
                    position = data["position"]
                    analyzer = VideoAnalyzer(detector, pose_estimator, character, position)

                    subtitles = []
                    for result in analyzer.analyze(output_path):
                        if result["command"]:
                            subtitles.append({
                                "frame": result["frame_idx"],
                                "text": result["command"],
                                "duration": 15
                            })

                    if not subtitles:
                        raise AppError(ErrorCode.NO_SUBTITLE, Messages.Error.NO_SUBTITLE)
                except AppError:
                    raise
                except Exception as e:
                    raise AppError(ErrorCode.ANALYZE_FAILED, Messages.Error.ANALYZE_FAILED)

                try:
                    await ffmpeg.overlay_subtitles(output_path, final_path, subtitles)
                except Exception as e:
                    raise AppError(ErrorCode.CUT_FAILED, Messages.Error.CUT_FAILED)

                try:
                    await s3.upload_file(str(final_path), processed_s3_key, config.aws.bucket_name)
                except Exception as e:
                    raise AppError(ErrorCode.UPLOAD_FAILED, Messages.Error.UPLOAD_FAILED)

            except AppError as e:
                message = { "email": data["email"], "detail": e.detail }
                try:
                    await rabbitmq.publish(message, RabbitMQConfig.VIDEO_RESULT)
                except Exception as e:
                    print(f"Failed to publish result: {e}")


