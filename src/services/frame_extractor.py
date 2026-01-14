import av
from io import BytesIO


def extract_frames(video_bytes):
    byte_stream = BytesIO(video_bytes)
    container = av.open(byte_stream)

    for frame in container.decode(video=0):
        img = frame.to_ndarray(format="rgb24")

        yield img
