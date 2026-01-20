import ffmpeg
from pathlib import Path
from typing import List


class FFmpegClient:
    async def cut(self, input_path: Path, output_path: Path, start: float, end: float) -> None:
        (
            ffmpeg
            .input(str(input_path), ss=start, t=end - start)
            .output(str(output_path))
            .run(quiet=True, overwrite_output=True)
        )

    async def overlay_subtitles(
        self,
        input_path: Path,
        output_path: Path,
        subtitles: List[dict],
        fps: float = 30.0
    ) -> None:
        drawtext_filters = []
        for sub in subtitles:
            start_time = sub["frame"] / fps
            duration = sub["duration"] / fps
            end_time = start_time + duration
            text = sub["text"]

            drawtext_filters.append(
                f"drawtext=text='{text}'"
                f":fontsize=48"
                f":fontcolor=white"
                f":borderw=2"
                f":bordercolor=black"
                f":x=(w-text_w)/2"
                f":y=h-100"
                f":enable='between(t,{start_time},{end_time})'"
            )

        filter_str = ",".join(drawtext_filters)

        (
            ffmpeg
            .input(str(input_path))
            .output(str(output_path), vf=filter_str)
            .run(quiet=True, overwrite_output=True)
        )
