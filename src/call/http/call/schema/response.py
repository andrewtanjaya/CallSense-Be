from typing import Any

from common.schema.base.response import BaseResponse, ListDataBaseResponseModel
from src.call.http.call.schema.model.call import (
    CallDetailResponseModel,
    CallResponseModel,
    EndedCallResponseModel,
    OngoingCallResponseModel,
    RecordingResponseModel,
)


class GetOngoingCalls(ListDataBaseResponseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data, message="Get ongoing calls successful")

    class Config:
        schema_extra = {
            "example": {
                "message": "Get ongoing calls successful",
                "data": [
                    OngoingCallResponseModel.Config.schema_extra.get("example")
                ],
            }
        }


class GetEndedCalls(ListDataBaseResponseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data, message="Get ended calls successful")

    class Config:
        schema_extra = {
            "example": {
                "message": "Get ended calls successful",
                "data": [
                    EndedCallResponseModel.Config.schema_extra.get("example")
                ],
            }
        }


class GetCallDetailsResponse(ListDataBaseResponseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data, message="Get call details successful")

    class Config:
        schema_extra = {
            "example": {
                "message": "Get call details successful",
                "data": [
                    CallDetailResponseModel.Config.schema_extra.get("example")
                ],
            }
        }


class GetRecordingsResponse(ListDataBaseResponseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data, message="Get recordings successful")

    class Config:
        schema_extra = {
            "example": {
                "message": "Get recordings successful",
                "data": [
                    RecordingResponseModel.Config.schema_extra.get("example")
                ],
            }
        }


class GetSentimentCallResponse(BaseResponse):
    category: str
    confidence: float

    def __init__(self, **data: Any) -> None:
        super().__init__(**data, message="Get sentiment result")

    class Config:
        schema_extra = {
            "example": {
                "message": "Get sentiment result",
                "category": "joy",
                "confidence": 0.98,
            }
        }
