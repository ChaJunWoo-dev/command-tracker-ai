from mmdet.apis import init_detector, inference_detector
from mmpose.apis import init_model, inference_topdown
from mmengine.registry import init_default_scope
from mmpose.utils.typing import ConfigDict

init_default_scope("mmdet")
init_default_scope("mmpose")

def adapt_mmdet_pipeline(cfg: ConfigDict) -> ConfigDict:
    from mmdet.datasets import transforms

    if "test_dataloader" not in cfg:
        return cfg

    pipeline = cfg.test_dataloader.dataset.pipeline

    for trans in pipeline:
        if trans["type"] in dir(transforms):
            trans["type"] = "mmdet." + trans["type"]

    return cfg

detect_config = "mmdetection/configs/rtmdet/rtmdet_m_8xb32-300e_coco.py"
detect_checkpoint = "models/rtmdet_m_8xb32-300e_coco_20220719_112220-229f527c.pth"
pose_config = "mmpose/configs/body_2d_keypoint/rtmpose/body8/rtmpose-l_8xb512-700e_body8-halpe26-384x288.py"
pose_checkpoint = "models/rtmpose-l_simcc-body7_pt-body7-halpe26_700e-384x288-734182ce_20230605.pth"

pose_model = init_model(pose_config, pose_checkpoint, device="cuda:0")
detector = init_detector(detect_config, detect_checkpoint, device="cuda:0")
detector.cfg = adapt_mmdet_pipeline(detector.cfg)

def analyze_frame(frame, side):
    mmdet_results = inference_detector(detector, frame)
    instances = mmdet_results.pred_instances
    bboxes = instances.bboxes.cpu().numpy()
    scores = instances.scores.cpu().numpy()

    person_results = []

    for bbox, score in zip(bboxes, scores):
        if score <= 0.3:
            continue

        x1, y1, x2, y2 = bbox[:4]
        area = (x2 - x1) * (y2 - y1)
        person_results.append({
            "bbox": [x1, y1, x2, y2],
            "bbox_score": float(score),
            "area": area
        })

    if len(person_results) == 0:
        return []

    person_results = sorted(person_results, key=lambda x: x["area"], reverse=True)[:2]
    person_results = sorted(person_results, key=lambda x: (x["bbox"][0] + x["bbox"][2]) / 2)

    if side == "left":
        selected = person_results[0]
    elif side == "right":
        selected = person_results[1]

    pose_results = inference_topdown(
        pose_model,
        frame,
        [selected["bbox"]],
        bbox_format="xyxy",
    )

    return pose_results
