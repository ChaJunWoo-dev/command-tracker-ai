import numpy as np
from typing import Tuple, Optional
from mmdet.apis import init_detector, inference_detector
from mmengine.registry import init_default_scope
from mmpose.utils.typing import ConfigDict


init_default_scope("mmdet")


def _adapt_mmdet_pipeline(cfg: ConfigDict) -> ConfigDict:
    """MMDetection과 MMPose의 transform registry 충돌을 해결하기 위해 네임스페이스 매핑"""
    from mmdet.datasets import transforms

    if "test_dataloader" not in cfg:
        return cfg

    pipeline = cfg.test_dataloader.dataset.pipeline

    for trans in pipeline:
        if trans["type"] in dir(transforms):
            trans["type"] = "mmdet." + trans["type"]

    return cfg


class PersonDetector:
    CONFIG = "third_party/mmdetection/configs/rtmdet/rtmdet_m_8xb32-300e_coco.py"
    CHECKPOINT = "models/rtmdet_m_8xb32-300e_coco_20220719_112220-229f527c.pth"

    def __init__(self, device: str = "cuda:0"):
        self._model = init_detector(self.CONFIG, self.CHECKPOINT, device=device)
        self._model.cfg = _adapt_mmdet_pipeline(self._model.cfg)

    def detect(
        self,
        frame: np.ndarray,
        score_threshold: float = 0.3,
        max_persons: Optional[int] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        프레임에서 사람 감지

        Returns:
            bboxes: 바운딩 박스 배열 (N, 4) - [x1, y1, x2, y2]
        """
        mmdet_results = inference_detector(self._model, frame)
        instances = mmdet_results.pred_instances

        person_mask = instances.labels.cpu().numpy() == 0
        bboxes = instances.bboxes.cpu().numpy()[person_mask]
        scores = instances.scores.cpu().numpy()[person_mask]

        valid_mask = scores > score_threshold
        bboxes = bboxes[valid_mask]

        # 영역 크기로 정렬 (큰 것부터)
        if len(bboxes) > 0 and max_persons is not None:
            areas = [(x2 - x1) * (y2 - y1) for x1, y1, x2, y2 in bboxes]
            top_indices = np.argsort(areas)[-max_persons:][::-1]
            bboxes = bboxes[top_indices]

        return bboxes
