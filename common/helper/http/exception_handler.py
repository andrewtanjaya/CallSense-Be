from typing import Union

from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import NoResultFound

from common.exception import mapping_exception_http_response
from common.schema.exception.entity import ErrorField
from common.schema.exception.response import (
    BadRequestResponse,
    NotFoundResponse,
    NotImplementedResponse,
    UnprocessableContentResponse,
)


def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        content=BadRequestResponse(
            message="invalid payload",
            error_fields=[
                _get_request_validation_error_field(error)
                for error in exc.errors()
            ],
        ).dict(),
        status_code=400,
    )


def _get_request_validation_error_field(error_dict: dict) -> ErrorField:
    try:
        loc = error_dict.get("loc", [])[1]
        msg = error_dict.get("msg")

        if isinstance(
            loc, int
        ):  # happened when payload have invalid structure
            loc = "body"
            msg = "invalid body payload"
    except IndexError:  # happened when payload is empty
        loc = "body"
        msg = "invalid body payload"

    return ErrorField(field=loc, message=msg)


def no_result_found_handler(
    request: Request, exc: NoResultFound
) -> JSONResponse:
    return JSONResponse(
        content=NotFoundResponse().dict(exclude_none=True), status_code=404
    )


def value_exception_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(
        content=UnprocessableContentResponse(message=str(exc)).dict(
            exclude_none=True
        ),
        status_code=422,
    )


def validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    return JSONResponse(
        content=UnprocessableContentResponse(
            message="validation error",
            error_fields=[
                _get_validation_error_field(error) for error in exc.errors()
            ],
        ).dict(),
        status_code=422,
    )


def _get_validation_error_field(error_dict: dict) -> ErrorField:
    try:
        locs = error_dict.get("loc", [])
        max_loc_index = len(locs)
        loc = locs[0]
        if loc == "__root__":
            loc = locs[max_loc_index - 1]
        msg = error_dict.get("msg")
    except IndexError:
        loc = "body"
        msg = "invalid body payload"

    if isinstance(loc, int):
        loc = "body"
        msg = "invalid body payload"

    return ErrorField(field=loc, message=msg)


def http_exception_handler(
    request: Request, exc: Union[RuntimeError, Exception]
) -> JSONResponse:
    return mapping_exception_http_response(exc)


def not_implemented_exception_handler(
    request: Request, exc: NotImplementedError
) -> JSONResponse:
    return JSONResponse(
        content=NotImplementedResponse().dict(exclude_none=True),
        status_code=501,
    )
