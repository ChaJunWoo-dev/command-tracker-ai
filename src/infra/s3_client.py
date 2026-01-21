import aioboto3
from botocore.config import Config
from config.settings import get_config
from config.constants import S3Config

config = get_config()


class S3Client:
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

    async def download_file(self, s3_key: str, dest_path: str, bucket: str) -> None:
        await self._client.download_file(bucket, s3_key, dest_path)

    async def upload_file(self, src_path: str, s3_key: str, bucket: str) -> None:
        await self._client.upload_file(src_path, bucket, s3_key)
