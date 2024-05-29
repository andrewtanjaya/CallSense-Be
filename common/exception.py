import json
from http import HTTPStatus
from typing import List, Optional

from fastapi.responses import JSONResponse

from common.schema.exception.entity import ErrorField
from common.schema.exception.response import (
    BaseResponse,
    ErrorCode,
    ErrorResponse,
    InternalServerErrorResponse,
    PageExceededMaxPageResponse,
)


class ExceptionWithData(RuntimeError):
    def __init__(self, **kwargs):
        self.data = kwargs

    def __str__(self) -> str:
        return json.dumps(self.data)

    def get_message(self) -> Optional[str]:
        return self.data.get("message")

    def get_fields(self) -> Optional[List[ErrorField]]:
        return self.data.get("error_fields") or []

    def get_headers(self) -> Optional[dict]:
        return self.data.get("headers")

    def get_extra_attributes(self) -> Optional[dict]:
        self.data.pop("message", None)
        self.data.pop("headers", None)
        self.data.pop("error_fields", None)
        return self.data


class BadRequestError(ExceptionWithData):
    pass


class PageExceededMaxPageError(ExceptionWithData):
    max_page: int
    total_records: int


class ConflictError(ExceptionWithData):
    pass


class ForbiddenError(ExceptionWithData):
    pass


class NotFoundError(ExceptionWithData):
    pass


class ServerError(ExceptionWithData):
    pass


class UnprocessableEntityError(ExceptionWithData):
    pass


class UnauthorizedError(ExceptionWithData):
    pass


class TooManyRequestError(ExceptionWithData):
    pass


status_code_map = {
    BadRequestError: HTTPStatus.BAD_REQUEST,
    PageExceededMaxPageError: HTTPStatus.BAD_REQUEST,
    UnauthorizedError: HTTPStatus.UNAUTHORIZED,
    ForbiddenError: HTTPStatus.FORBIDDEN,
    NotFoundError: HTTPStatus.NOT_FOUND,
    ConflictError: HTTPStatus.CONFLICT,
    TooManyRequestError: HTTPStatus.TOO_MANY_REQUESTS,
    ServerError: HTTPStatus.INTERNAL_SERVER_ERROR,
}


def mapping_exception_http_response(error: RuntimeError) -> JSONResponse:
    code = status_code_map.get(type(error)) or HTTPStatus.INTERNAL_SERVER_ERROR

    response_obj: BaseResponse
    if isinstance(error, PageExceededMaxPageError):
        response_obj = PageExceededMaxPageResponse(
            message=error.get_message() or code.phrase,
            **error.get_extra_attributes(),
        )

    elif isinstance(error, ExceptionWithData):
        response_obj = ErrorResponse(
            message=error.get_message() or code.phrase,
            error_code=ErrorCode(code.value).name,
            error_fields=error.get_fields(),
        )

    else:
        response_obj = InternalServerErrorResponse()

    return JSONResponse(
        content=response_obj.dict(),
        status_code=code.value,
        headers=error.get_headers()
        if isinstance(error, ExceptionWithData)
        else None,
    )
