import ffmpeg
from pathlib import Path


class FFmpegClient:
    async def cut(self, input_path: Path, output_path: Path, start: float, end: float) -> None:
        (
            ffmpeg
            .input(str(input_path), ss=start, t=end - start)
            .output(str(output_path))
            .run(quiet=True)
        )
