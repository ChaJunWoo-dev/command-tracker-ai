import aioboto3
from botocore.config import Config
from config.env import get_config
from config.constants import S3Config

config = get_config()


class S3Manager:
    def __init__(self):
        self._session = aioboto3.Session()
        self._region = config.aws.region
        self._client = None

    async def __aenter__(self):
        self._client = await self._session.client(
            "s3",
            region_name=self._region,
            config=Config(signature_version="s3v4"),
        ).__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._client:
            await self._client.__aexit__(exc_type, exc, tb)
            self._client = None

    async def download_stream(self, blob_s3_key: str, bucket: str):
        obj = await self._client.get_object(
            Bucket=bucket,
            Key=blob_s3_key,
        )
        body = obj["Body"]

        while True:
            chunk = await body.read(1024 * 1024)
            if not chunk:
                break
            yield chunk

    async def get_presigned_url(self, blob_s3_key: str, bucket: str) -> str:
        return await self._client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": bucket,
                "Key": blob_s3_key,
            },
            ExpiresIn=S3Config.SIGNED_URL_EXPIRE,
        )

    async def upload_stream(self, blob_s3_key: str, stream, bucket: str) -> str:
        upload_id = None
        try:
            response = await self._client.create_multipart_upload(
                Bucket=bucket,
                Key=blob_s3_key,
                ContentType="video/webm",
            )
            upload_id = response["UploadId"]

            parts = []
            part_number = 1

            async for chunk in stream:
                if not chunk:
                    continue

                part_response = await self._client.upload_part(
                    Bucket=bucket,
                    Key=blob_s3_key,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=chunk,
                )

                parts.append(
                    {
                        "PartNumber": part_number,
                        "ETag": part_response["ETag"],
                    }
                )
                part_number += 1

            await self._client.complete_multipart_upload(
                Bucket=bucket,
                Key=blob_s3_key,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts},
            )

            return f"s3://{bucket}/{blob_s3_key}"

        except Exception:
            if upload_id:
                try:
                    await self._client.abort_multipart_upload(
                        Bucket=bucket,
                        Key=blob_s3_key,
                        UploadId=upload_id,
                    )
                except Exception:
                    pass
            raise
