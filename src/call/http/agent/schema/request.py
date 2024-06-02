from typing import Optional

from common.schema.base.response import BaseWithConfig


class InitiateCallRequest(BaseWithConfig):
    customer_streaming_url: Optional[str]
    agent_streaming_url: Optional[str]

    class Config(BaseWithConfig.Config):
        schema_extra = {
            "example": {
                "customer_streaming_url": "https://api.example.com/streaming",
                "agent_streaming_url": "https://api.example.com/streaming",
            }
        }
