import ffmpeg
import io
from config.constants import MESSAGES


def frames_to_timecode(frame, fps):
    total_seconds = frame / fps
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    cs = int((total_seconds - int(total_seconds)) * 100)

    return f"{h}:{m:02}:{s:02}.{cs:02}"


def make_stack_ass(commands, file_name, fps=30, max_stack=10):
    try:
        header = """[Script Info]
            Title: Command Subtitle
            ScriptType: v4.00+
            Collisions: Normal
            PlayDepth: 0

            [V4+ Styles]
            Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
            Style: Default,Arial,14,&H00FFFFFF,&H000000FF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,1,0,7,20,10,30,1

            [Events]
            Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
            """

        events = ""

        for i in range(len(commands)):
            stack_slice = commands[max(0, i - max_stack + 1):i + 1]
            stack_labels = [c["label"] for c in stack_slice]
            text = r"\N".join(stack_labels)

            start_frame = commands[i]["start_frame"]

            if i + 1 < len(commands):
                end_frame = commands[i + 1]["start_frame"]
            else:
                commands[i]["end_frame"] + fps * 2

            start_tc = frames_to_timecode(start_frame, fps)
            end_tc = frames_to_timecode(end_frame, fps)

            events += f"Dialogue: 0,{start_tc},{end_tc},Default,,0,0,0,,{text}\n"

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(header + events)
    except:
        raise RuntimeError(MESSAGES.ERROR.FAILED_CREATE_SUBTITLE)


def insert_subtitle_to_video(video_bytes, subtitle_path):
    try:
        input_video = ffmpeg.input("pipe:0")

        output, _ = (
            input_video
            .filter("subtitles", subtitle_path)
            .output("pipe:1",
                    vcodec="libvpx-vp9",
                    acodec="libvorbis",
                    format="webm")
            .run(input=video_bytes, capture_stdout=True)
        )

        return io.BytesIO(output)

    except:
        raise RuntimeError(MESSAGES.ERROR.FAILED_INSERT_SUBTITLE)
