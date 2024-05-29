from http import HTTPStatus
from typing import Any, Dict, List, Optional

from common.schema.base.response import BaseResponse
from common.schema.exception.entity import ErrorField
from common.schema.exception.enum import ErrorCode


class ErrorResponse(BaseResponse):
    error_code: str
    error_fields: Optional[List[ErrorField]]

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.message = data.get("message")

    class Config(BaseResponse.Config):
        schema_extra = {
            "example": {
                "message": "human readable error message",
                "error_code": ErrorCode.INTERNAL_SERVER_ERROR.name,
                "error_fields": [
                    ErrorField.Config.schema_extra.get("example")
                ],
            }
        }


class BadRequestResponse(ErrorResponse):
    def __init__(self, **data: Any) -> None:
        super().__init__(
            **data,
            error_code=ErrorCode.INVALID_PAYLOAD.name,
        )
        self.message = (
            data.get("message") or HTTPStatus.BAD_REQUEST.description
        )

    class Config(BaseResponse.Config):
        schema_extra = {
            "message": "error validation on registration process",
            "error_code": "INVALID_PAYLOAD",
            "error_fields": [
                {
                    "field": "email",
                    "message": "email must filled with email format",
                },
                {
                    "field": "some_foo_attribute",
                    "message": "some foo attribute is required",
                },
            ],
        }


class PageExceededMaxPageResponse(BaseResponse):
    data: Optional[Dict[str, List]] = {"data": []}
    max_page: Optional[int] = 0
    total_records: Optional[int] = 0

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.message = data.get("message") or "page exceeded max page"

    class Config(BaseResponse.Config):
        schema_extra = {
            "example": {
                "message": "page exceeded max page",
                "data": {"data": []},
                "max_page": 0,
                "total_records": 0,
            }
        }


class UnauthorizedResponse(ErrorResponse):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data, error_code=ErrorCode.UNAUTHORIZED.name)
        self.message = (
            data.get("message") or HTTPStatus.UNAUTHORIZED.description
        )

    class Config(BaseResponse.Config):
        schema_extra = {
            "example": {
                "message": "unauthorized",
                "error_code": ErrorCode.UNAUTHORIZED.name,
            }
        }


class NotFoundResponse(ErrorResponse):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data, error_code=ErrorCode.NOT_FOUND.name)
        self.message = data.get("message") or "data not found"

    class Config(BaseResponse.Config):
        schema_extra = {
            "example": {
                "message": "account not found",
                "error_code": ErrorCode.NOT_FOUND,
            }
        }


class ConflictResponse(ErrorResponse):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data, error_code=ErrorCode.CONFLICT.name)
        self.message = data.get("message") or HTTPStatus.CONFLICT.description

    class Config(BaseResponse.Config):
        schema_extra = {
            "example": {
                "message": HTTPStatus.CONFLICT.description,
                "error_code": ErrorCode.CONFLICT.name,
            }
        }


class UnprocessableContentResponse(ErrorResponse):
    def __init__(self, **data):
        super().__init__(
            **data, error_code=ErrorCode.UNPROCESSABLE_CONTENT.name
        )
        self.message = (
            data.get("message") or HTTPStatus.UNPROCESSABLE_ENTITY.description
        )

    class Config(BaseResponse.Config):
        schema_extra = {
            "example": {
                "message": "validation error",
                "error_code": ErrorCode.UNPROCESSABLE_CONTENT.name,
                "error_fields": [
                    {
                        "field": "email",
                        "message": "email must filled with email format",
                    },
                    {
                        "field": "some_foo_attribute",
                        "message": "some foo attribute is required",
                    },
                ],
            }
        }


class InternalServerErrorResponse(ErrorResponse):
    def __init__(self, **data: Any) -> None:
        super().__init__(
            **data, error_code=ErrorCode.INTERNAL_SERVER_ERROR.name
        )
        self.message = data.get("message") or "internal server error"

    class Config(BaseResponse.Config):
        schema_extra = {
            "example": {
                "message": "internal server error",
                "error_code": ErrorCode.INTERNAL_SERVER_ERROR,
            }
        }


class NotImplementedResponse(ErrorResponse):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data, error_code=ErrorCode.NOT_IMPLEMENTED.name)
        self.message = (
            data.get("message") or HTTPStatus.NOT_IMPLEMENTED.description
        )

    class Config(BaseResponse.Config):
        schema_extra = {
            "example": {
                "message": HTTPStatus.NOT_IMPLEMENTED.description,
                "error_code": ErrorCode.NOT_IMPLEMENTED.name,
            }
        }
