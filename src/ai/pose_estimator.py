"""
MMPose 기반 포즈 추정 모듈
"""
import numpy as np
from typing import List
from mmpose.apis import init_model, inference_topdown
from mmengine.registry import init_default_scope


init_default_scope("mmpose")


class PoseEstimator:
    CONFIG = "third_party/mmpose/projects/rtmpose/rtmpose/body_2d_keypoint/rtmpose-l_8xb256-420e_coco-256x192.py"
    CHECKPOINT = "models/rtmpose-l_8xb256-420e_humanart-256x192-389f2cb0_20230611.pth"

    def __init__(self, device: str = "cuda:0"):
        self._model = init_model(self.CONFIG, self.CHECKPOINT, device=device)

    def estimate(self, frame: np.ndarray, bboxes: np.ndarray) -> List:
        """
        바운딩 박스에 대해 포즈 추정

        Args:
            frame: 입력 프레임
            bboxes: 바운딩 박스 배열 (N, 4) - [x1, y1, x2, y2]

        Returns:
            pose_results: MMPose 포즈 추정 결과 리스트
        """
        if len(bboxes) == 0:
            return []

        return inference_topdown(
            self._model,
            frame,
            bboxes.tolist(),
            bbox_format="xyxy"
        )
