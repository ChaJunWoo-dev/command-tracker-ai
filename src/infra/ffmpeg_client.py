import asyncio
import subprocess
from pathlib import Path


class FFmpegClient:
    def __init__(self, ffmpeg_path: str = "ffmpeg", ffprobe_path: str = "ffprobe"):
        self._ffmpeg_path = ffmpeg_path
        self._ffprobe_path = ffprobe_path

    async def run_command(self, args: list[str]) -> tuple[str, str]:
        cmd = [self._ffmpeg_path] + args
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {stderr.decode()}")

        return stdout.decode(), stderr.decode()

    async def probe(self, path: str | Path) -> dict:
        import json

        cmd = [
            self._ffprobe_path,
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            str(path),
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"FFprobe failed: {stderr.decode()}")

        return json.loads(stdout.decode())

    async def get_duration(self, path: str | Path) -> float:
        info = await self.probe(path)
        return float(info["format"]["duration"])

    async def get_resolution(self, path: str | Path) -> tuple[int, int]:
        info = await self.probe(path)
        for stream in info["streams"]:
            if stream["codec_type"] == "video":
                return stream["width"], stream["height"]
        raise ValueError("No video stream found")
