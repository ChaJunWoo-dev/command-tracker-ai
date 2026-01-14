def filter_frame(frames):
    if not frames:
        return []

    filtered_frames = []
    prev = frames[0]
    group_start = prev

    for i in range(1, len(frames)):
        if frames[i] - prev > 1:
            if group_start != prev:
                filtered_frames.append(group_start)
            group_start = frames[i]
        prev = frames[i]

    if group_start != prev:
        filtered_frames.append(group_start)

    return filtered_frames


def get_commands(sit_punch_frames, uppercut_frames, hit_down_frames):
    commands = []
    fps = 30

    for frame in filter_frame(sit_punch_frames):
        commands.append({
            "start_frame": frame,
            "end_frame": frame + fps * 2,
            "label": "↓ + [LP]"
        })

    for frame in filter_frame(uppercut_frames):
        commands.append({
            "start_frame": frame,
            "end_frame": frame + fps * 2,
            "label": "↓↙← + P"
        })

    for frame in filter_frame(hit_down_frames):
        commands.append({
            "start_frame": frame,
            "end_frame": frame + fps * 2,
            "label": "→ + P"
        })

    return commands
