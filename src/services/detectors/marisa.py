def detect(angles, commands):
    """마리사 커맨드 검출"""
    gladius = commands["Gladius"]["angles"]
    if (
        angles["r_elbow"] > gladius["r_elbow_min"] and angles["l_elbow"] < gladius["l_elbow_max"] and
        angles["l_knee"] < gladius["l_knee_max"] and angles["r_knee"] > gladius["r_knee_min"]
    ):
        return "Gladius", commands["Gladius"]["cooldown"]

    quadriga = commands["Quadriga"]["angles"]
    if (
        angles["r_elbow"] > quadriga["r_elbow_min"] and angles["l_elbow"] > quadriga["l_elbow_min"] and
        angles["r_knee"] > quadriga["r_knee_min"] and angles["l_knee"] > quadriga["l_knee_min"] and
        angles["body_lean"] < quadriga["body_lean_max"]
    ):
        return "Quadriga", commands["Quadriga"]["cooldown"]

    heavy_kick = commands["HeavyKick"]["angles"]
    if (
        angles["l_elbow"] < heavy_kick["l_elbow_max"] and
        angles["l_knee"] > heavy_kick["l_knee_min"] and angles["r_knee"] > heavy_kick["r_knee_min"]
    ):
        return "HeavyKick", commands["HeavyKick"]["cooldown"]

    crouch = commands["Crouch"]["angles"]
    if (
        crouch["l_elbow_min"] < angles["l_elbow"] < crouch["l_elbow_max"] and
        crouch["r_elbow_min"] < angles["r_elbow"] < crouch["r_elbow_max"] and
        crouch["l_knee_min"] < angles["l_knee"] < crouch["l_knee_max"] and
        crouch["r_knee_min"] < angles["r_knee"] < crouch["r_knee_max"]
    ):
        return "Crouch", commands["Crouch"]["cooldown"]

    return None, 0
