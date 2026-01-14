import math


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def angle_between_points(a, b, c):
    ba = (a[0] - b[0], a[1] - b[1])
    bc = (c[0] - b[0], c[1] - b[1])
    cos_angle = (ba[0] * bc[0] + ba[1] * bc[1]) / (dist(a, b) * dist(c, b) + 1e-6)
    angle = math.acos(max(min(cos_angle, 1), -1))

    return math.degrees(angle)


def label_frames(pose_data, frame_id, sit_punch_frames, uppercut_frames, hit_down_frames):
    keypoints = pose_data[0].pred_instances.keypoints[0]

    left_shoulder = keypoints[5]
    right_shoulder = keypoints[6]
    left_elbow = keypoints[7]
    right_elbow = keypoints[8]
    left_wrist = keypoints[9]
    right_wrist = keypoints[10]
    left_hip = keypoints[11]
    right_hip = keypoints[12]
    left_knee = keypoints[13]
    right_knee = keypoints[14]
    left_ankle = keypoints[15]
    right_ankle = keypoints[16]
    head = keypoints[17]
    neck = keypoints[18]
    hip = keypoints[19]

    left_arm_angle = angle_between_points(left_shoulder, left_elbow, left_wrist)
    right_arm_angle = angle_between_points(right_shoulder, right_elbow, right_wrist)
    left_knee_angle = angle_between_points(left_hip, left_knee, left_ankle)
    right_knee_angle = angle_between_points(right_hip, right_knee, right_ankle)

    if 150 < left_arm_angle < 180 and 0 < right_arm_angle < 15 and 75 < left_knee_angle < 105 and 135 < right_knee_angle < 165:
        sit_punch_frames.append(frame_id)

    if right_shoulder[0] > neck[0] and head[1] - right_wrist[1] > 140 and right_elbow[1] < head[1] and left_shoulder[1] > right_shoulder[1] and 90 < left_knee_angle < 130 and 110 < right_knee_angle < 160:
        uppercut_frames.append(frame_id)

    if 120 < right_knee_angle < 170 and neck[0] > hip[0] and right_shoulder[1] < neck[1] < left_shoulder[1] and 40 < right_arm_angle < 110 and right_ankle[1] - neck[1] < 300:
        hit_down_frames.append(frame_id)
