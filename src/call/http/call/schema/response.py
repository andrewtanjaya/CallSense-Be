from typing import Any

from common.schema.base.response import ListDataBaseResponseModel
from src.call.http.call.schema.model.call import (
    CallDetailResponseModel,
    CallResponseModel,
    EndedCallResponseModel,
    RecordingResponseModel,
)


class GetOngoingCalls(ListDataBaseResponseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data, message="Get ongoing calls successful")

    class Config:
        schema_extra = {
            "example": {
                "message": "Get ongoing calls successful",
                "data": [CallResponseModel.Config.schema_extra.get("example")],
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
