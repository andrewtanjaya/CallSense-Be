from typing import Optional

from common.schema.base.response import BaseWithConfig


class InitiateCallRequest(BaseWithConfig):
    streaming_url: Optional[str]

    class Config(BaseWithConfig.Config):
        schema_extra = {
            "example": {
                "streaming_url": "https://api.example.com/streaming",
            }
        }
