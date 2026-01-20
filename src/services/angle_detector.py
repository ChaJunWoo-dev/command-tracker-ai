import math
from config.constants import Keypoints, CHARACTER_CONFIG
from services.detectors import DETECTORS


def calculate_angle(p1, p2, p3) -> float:
    """세 점으로 각도 계산 (관절들의 각 점)"""
    v1 = (p1[0] - p2[0], p1[1] - p2[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])

    dot = v1[0] * v2[0] + v1[1] * v2[1]
    mag1 = math.sqrt(v1[0] ** 2 + v1[1] ** 2)
    mag2 = math.sqrt(v2[0] ** 2 + v2[1] ** 2)

    if mag1 == 0 or mag2 == 0:
        return 0.0

    cos_angle = max(-1.0, min(1.0, dot / (mag1 * mag2)))
    return math.degrees(math.acos(cos_angle))


def extract_angles(kpts):
    l_shoulder = kpts[Keypoints.LEFT_SHOULDER]
    r_shoulder = kpts[Keypoints.RIGHT_SHOULDER]
    l_elbow = kpts[Keypoints.LEFT_ELBOW]
    r_elbow = kpts[Keypoints.RIGHT_ELBOW]
    l_wrist = kpts[Keypoints.LEFT_WRIST]
    r_wrist = kpts[Keypoints.RIGHT_WRIST]
    l_hip = kpts[Keypoints.LEFT_HIP]
    r_hip = kpts[Keypoints.RIGHT_HIP]
    l_knee = kpts[Keypoints.LEFT_KNEE]
    r_knee = kpts[Keypoints.RIGHT_KNEE]
    l_ankle = kpts[Keypoints.LEFT_ANKLE]
    r_ankle = kpts[Keypoints.RIGHT_ANKLE]

    return {
        "l_elbow": calculate_angle(l_shoulder, l_elbow, l_wrist),
        "r_elbow": calculate_angle(r_shoulder, r_elbow, r_wrist),
        "l_knee": calculate_angle(l_hip, l_knee, l_ankle),
        "r_knee": calculate_angle(r_hip, r_knee, r_ankle),
        "body_lean": (l_hip[1] + r_hip[1]) / 2 - (l_shoulder[1] + r_shoulder[1]) / 2,
    }


class AngleBasedDetector:
    def __init__(self, character: str, position: str = "left"):
        self.config = CHARACTER_CONFIG[character]
        self.detector = DETECTORS[character]
        self.position = position
        self.cooldown = 0

    def detect(self, kpts):
        if self.cooldown > 0:
            self.cooldown -= 1
            return None

        angles = extract_angles(kpts)
        debug(angles)

        command, cooldown = self.detector(angles, self.config)
        if command:
            self.cooldown = cooldown
        return command


def debug(angles):
    print(f"[DEBUG] L_elbow: {angles['l_elbow']:.0f}° R_elbow: {angles['r_elbow']:.0f}° | L_knee: {angles['l_knee']:.0f}° R_knee: {angles['r_knee']:.0f}° | lean: {angles['body_lean']:.0f}")
