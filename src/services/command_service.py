from services.angle_detector import AngleBasedDetector
from typing import Union, List


class MotionRecognizer:
    def __init__(self, character: str, position: str = "left"):
        self.character = character
        self.detector = AngleBasedDetector(character, position)

    def extract(self, pose) -> Union[str, None]:
        """
        포즈 시퀀스를 기반으로 현재 프레임의 캐릭터 동작을 판정

        Args: MMPose의 PoseDataSample (관절 좌표 + score)
        return: 판정된 동작 문자열 예) "GLADIUS"
        """
        kpts = pose.pred_instances.keypoints[0]

        return self.detector.detect(kpts)

    def get_input(self, command: str) -> List[str]:
        """커맨드의 입력 시퀀스 반환"""
        return self.detector.get_input(command)
