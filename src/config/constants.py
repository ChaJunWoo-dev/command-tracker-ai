class S3Config:
    SIGNED_URL_EXPIRE = 60 * 24


class RabbitMQConfig:
    HEART_BEAT = 60
    VIDEO_PROCESS = "video_process_queue"
    VIDEO_RESULT = "video_result_queue"


class Messages:
    class Success:
        ANALYZE = "영상 분석을 완료했습니다."

    class Error:
        RABBITMQ_NOT_INIT = "RabbitMQ 미초기화. init_rabbitmq()를 호출하세요."

        NOT_FOUND_VIDEO = "영상을 찾을 수 없습니다."
        FAILED_ANALYZE = "영상 분석에 실패했습니다."
        FAILED_UPLOAD = "영상 저장에 실패했습니다."
        FAILED_GENERATE_URL = "액세스 링크 생성에 실패했습니다."

        FAILED_INSERT_SUBTITLE = "영상에 자막을 삽입하는 데 실패했습니다."
        FAILED_CREATE_SUBTITLE = "자막 파일 생성에 실패했습니다."

        SERVER_ERROR = "서버 오류가 발생했습니다."


class ResultCode:
    class Success:
        ANALYZE = "SUCCESS_ANALYZE"

    class Failed:
        ANALYZE = "FAILED_ANALYZE"
