import ffmpeg
from pathlib import Path


class FFmpegClient:
    async def cut(self, input_path: Path, output_path: Path, start: float, end: float) -> None:
        (
            ffmpeg
            .input(str(input_path), ss=start, to=end)
            .output(str(output_path), c="copy")
            .overwrite_output()
            .run(quiet=True)
        )
