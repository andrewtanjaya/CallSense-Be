import logging
from contextlib import asynccontextmanager
from sys import stderr as sys_stderr
from sys import stdout as sys_stdout
from time import time

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic.error_wrappers import ValidationError
from sqlalchemy.exc import NoResultFound

from __init__ import __version__
from common.constant import EXCLUDED_HANDLERS
from common.dependencies import get_database
from common.helper.http.exception_handler import (
    http_exception_handler,
    no_result_found_handler,
    not_implemented_exception_handler,
    request_validation_exception_handler,
    validation_exception_handler,
    value_exception_handler,
)
from common.schema.base.response import SuccessResponse
from src.router import router


def set_log():
    logger = logging.getLogger("uvicorn.access")
    if logger.handlers:
        logger.handlers.pop()
        handler = logging.StreamHandler(sys_stdout)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)

    logger = logging.getLogger("uvicorn")
    if logger.handlers:
        logger.handlers.pop()
        handler = logging.StreamHandler(sys_stderr)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)


def init_exception_handler(app: FastAPI):
    app.add_exception_handler(
        RequestValidationError, request_validation_exception_handler
    )
    app.add_exception_handler(ValueError, value_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(NoResultFound, no_result_found_handler)
    app.add_exception_handler(RuntimeError, http_exception_handler)
    app.add_exception_handler(Exception, http_exception_handler)
    app.add_exception_handler(
        NotImplementedError, not_implemented_exception_handler
    )


def create_app() -> FastAPI:
    app = FastAPI(
        title="Hackathon BI Documentation",
        version=__version__,
        docs_url="/v1/docs",
        redoc_url="/v1/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["content-disposition"],
    )

    app.include_router(router)
    init_exception_handler(app)

    set_log()

    return app


app = create_app()


# @asynccontextmanager
# async def startup_event():
#     Instrumentator(
#         excluded_handlers=EXCLUDED_HANDLERS,
#         should_group_status_codes=False,
#     ).instrument(app).expose(
#         app=app,
#         tags=["prometheus"],
#         include_in_schema=False,
#     )


@app.get("/health", status_code=200, response_model=SuccessResponse)
def health_check(resp: Response):
    return SuccessResponse(message="OK")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def remove_session(request: Request, call_next):
    response = await call_next(request)
    get_database().get_session().remove()
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
