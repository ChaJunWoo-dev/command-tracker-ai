def detect(angles, config):
    """마리사 커맨드 검출"""
    angle_config = config["angles"]
    cooldown = config["cooldown"]

    gladius = angle_config["Gladius"]
    if (
        angles["r_elbow"] > gladius["r_elbow_min"] and angles["l_elbow"] < gladius["l_elbow_max"] and
        angles["l_knee"] < gladius["l_knee_max"] and angles["r_knee"] > gladius["r_knee_min"]
    ):
        return "Gladius", cooldown["Gladius"]

    quadriga = angle_config["Quadriga"]
    if (
        angles["r_elbow"] > quadriga["r_elbow_min"] and angles["l_elbow"] > quadriga["l_elbow_min"] and
        angles["r_knee"] > quadriga["r_knee_min"] and angles["l_knee"] > quadriga["l_knee_min"] and
        angles["body_lean"] < quadriga["body_lean_max"]
    ):
        return "Quadriga", cooldown["Quadriga"]

    return None, 0
