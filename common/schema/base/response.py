from http import HTTPStatus
from typing import Any, Optional

from orjson import dumps as orjson_dumps
from orjson import loads as orjson_loads
from pydantic import BaseModel

from common.schema.base.entity import (
    ListDataBaseResponseModel,
    ListDataCursorBaseResponseModel,
)


def _orjson_dumps(v, *, default):
    return orjson_dumps(v, default=default).decode()


class BaseWithConfig(BaseModel):
    class Config:
        json_loads = orjson_loads
        json_dumps = _orjson_dumps


class BaseResponse(BaseWithConfig):
    message: Optional[str]

    class Config(BaseWithConfig.Config):
        schema_extra = {
            "example": {
                "message": "some message",
            }
        }


class SuccessResponse(BaseResponse):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.message = data.get("message") or HTTPStatus.OK.description

    class Config(BaseResponse.Config):
        schema_extra = {
            "example": {
                "message": "success message",
            }
        }


class CreatedResponse(BaseResponse):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.message = data.get("message") or HTTPStatus.CREATED.description

    class Config(BaseResponse.Config):
        schema_extra = {
            "example": {
                "message": "created message",
            }
        }


class ListBaseResponse(BaseResponse):
    data: Optional[ListDataBaseResponseModel] = {}

    def __init__(self, **data: Any) -> None:
        super().__init__(
            data=ListDataBaseResponseModel(data=data.get("data") or []),
            message=data.get("message") or "get list successful",
        )

    class Config(BaseResponse.Config):
        schema_extra = {
            "example": {
                "message": "get list successful",
                "data": {
                    "data": [],
                },
            }
        }


class ListCursorPaginationBaseResponse(BaseResponse):
    data: Optional[ListDataCursorBaseResponseModel]

    def __init__(self, **data: Any) -> None:
        super().__init__(
            message=data.get("message")
            or "get list cursor pagination successful",
        )
        self.data = ListDataCursorBaseResponseModel(
            data=data.get("data") or [],
            is_last=data.get("is_last"),
            total_records=data.get("total_records"),
        )

    class Config(BaseResponse.Config):
        schema_extra = {
            "example": {
                "message": "get list successful",
                "data": {
                    "data": [],
                    "is_last": True,
                    "last_id": None,
                    "total_records": 0,
                },
            }
        }
