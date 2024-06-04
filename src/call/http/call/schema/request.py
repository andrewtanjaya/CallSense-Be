from common.schema.base.response import BaseWithConfig


class CallDetailSentimentRequest(BaseWithConfig):
    file_path: str

    class Config(BaseWithConfig.Config):
        schema_extra = {
            "example": {
                "file_path": "path/to/file",
            }
        }
