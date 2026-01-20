class S3Config:
    SIGNED_URL_EXPIRE = 60 * 24
    ORIGINAL_PREFIX = "original"
    PROCESSED_PREFIX = "processed"


class RabbitMQConfig:
    HEART_BEAT = 60
    VIDEO_PROCESS = "video_process_queue"
    VIDEO_RESULT = "video_result_queue"


class Messages:
    class Success:
        ANALYZE = "영상 분석을 완료했습니다."

    class Error:
        RABBITMQ_NOT_READY = "RabbitMQ 미초기화. init_rabbitmq()를 호출하세요."

        DOWNLOAD_FAILED = "영상 다운로드에 실패했습니다."
        CUT_FAILED = "영상 자르기에 실패했습니다."
        UPLOAD_FAILED = "영상 업로드에 실패했습니다."
        ANALYZE_FAILED = "영상 분석에 실패했습니다."
        NO_SUBTITLE = "지원하지 않는 동작이거나 인식에 실패했습니다."
        SERVER_ERROR = "작업 처리 중 내부 오류가 발생했습니다."


class ErrorCode:
    DOWNLOAD_FAILED = "DOWNLOAD_FAILED"
    CUT_FAILED = "CUT_FAILED"
    ANALYZE_FAILED = "ANALYZE_FAILED"
    UPLOAD_FAILED = "UPLOAD_FAILED"
    NO_SUBTITLE = "NO_SUBTITLE"
    WORKER_CRASH = "WORKER_CRASH"


class ResultCode:
    class Success:
        ANALYZE = "SUCCESS_ANALYZE"

    class Failed:
        ANALYZE = "FAILED_ANALYZE"


class TempDir:
    BASE_DIR = None


class Keypoints:
    NOSE = 0

    LEFT_EYE = 1
    RIGHT_EYE = 2

    LEFT_EAR = 3
    RIGHT_EAR = 4

    LEFT_SHOULDER = 5
    RIGHT_SHOULDER = 6

    LEFT_ELBOW = 7
    RIGHT_ELBOW = 8

    LEFT_WRIST = 9
    RIGHT_WRIST = 10

    LEFT_HIP = 11
    RIGHT_HIP = 12

    LEFT_KNEE = 13
    RIGHT_KNEE = 14

    LEFT_ANKLE = 15
    RIGHT_ANKLE = 16


CHARACTER_CONFIG = {
    "MARISA": {
        "commands": ["Gladius", "Quadriga", "Phalanx", "Scutum"],
        "cooldown": {
            "Gladius": 21,
            "Quadriga": 24,
        },
        "angles": {
            "Gladius": {
                "r_elbow_min": 150,
                "l_elbow_max": 100,
                "l_knee_max": 110,
                "r_knee_min": 150,
            },
            "Quadriga": {
                "r_elbow_min": 150,
                "l_elbow_min": 150,
                "r_knee_min": 140,
                "l_knee_min": 140,
                "body_lean_max": 50,
            },
        },
    },
}
