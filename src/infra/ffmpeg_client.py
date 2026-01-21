import ffmpeg
from pathlib import Path
from typing import List


class FFmpegClient:
    STACK_MARGIN = 10
    MAX_STACK = 10
    ICON_HEIGHT = 64
    FPS = 30

    async def cut(self, input_path: Path, output_path: Path, start: float, end: float) -> None:
        (
            ffmpeg
            .input(str(input_path), ss=start, t=end - start)
            .output(str(output_path))
            .run(quiet=True, overwrite_output=True)
        )

    async def overlay_images(
        self,
        input_path: Path,
        output_path: Path,
        overlays: List[dict],
    ) -> None:
        """
        이미지를 영상 왼쪽에 스택 형태로 오버레이
        최신 커맨드가 위에 쌓임
        overlays: [{"frame": int, "image_path": Path}, ...]
        """
        input_stream = ffmpeg.input(str(input_path))

        current = input_stream.video
        for stack_idx, overlay in enumerate(overlays):
            start_time = overlay["frame"] / self.FPS
            image_path = overlay["image_path"]

            # y값이 작을수록 위에 위치
            y_pos = f"H-{self.STACK_MARGIN}-{(stack_idx + 1) * (self.ICON_HEIGHT + self.STACK_MARGIN)}"

            img_input = ffmpeg.input(str(image_path))

            current = ffmpeg.overlay(
                current,
                img_input,
                x=str(self.STACK_MARGIN),
                y=y_pos,
                enable=f"gte(t,{start_time})"
            )

        ffmpeg \
            .output(current, input_stream.audio, str(output_path)) \
            .run(quiet=True, overwrite_output=True)

