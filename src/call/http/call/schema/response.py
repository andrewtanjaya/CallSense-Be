from typing import Any

from common.schema.base.response import ListDataBaseResponseModel
from src.call.http.call.schema.model.call import (
    CallDetailResponseModel,
    CallsResponseModel,
    RecordingResponseModel,
)


class GetCallsResponse(ListDataBaseResponseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data, message="Get calls successful")

    class Config:
        schema_extra = {
            "example": {
                "message": "Get notifications successful",
                "data": [
                    CallsResponseModel.Config.schema_extra.get("example")
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
