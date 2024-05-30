from uuid import UUID

from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter

from common.schema.exception.response import (
    BadRequestResponse,
    InternalServerErrorResponse,
    NotFoundResponse,
)
from src.call.adapter.uow import SQLAlchemyUnitOfWork
from src.call.http.call.schema.response import (
    CallDetailResponseModel,
    CallResponseModel,
    EndedCallResponseModel,
    GetCallDetailsResponse,
    GetEndedCalls,
    GetOngoingCalls,
    GetRecordingsResponse,
    RecordingResponseModel,
)
from src.call.service import call as call_service

router = APIRouter(
    default_response_class=ORJSONResponse,
    prefix="/calls",
    tags=["calls"],
    redirect_slashes=False,
)


@router.get(
    "/ended",
    status_code=200,
    responses={
        200: {"model": GetEndedCalls},
        400: {"model": BadRequestResponse},
        404: {"model": NotFoundResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
def get_all_ended_calls():
    calls = call_service.get_ended_calls(SQLAlchemyUnitOfWork())

    return GetEndedCalls(
        data=[
            EndedCallResponseModel(**call_entity.dict())
            for call_entity in calls
        ],
    )


@router.get(
    "/ongoing",
    status_code=200,
    responses={
        200: {"model": GetOngoingCalls},
        400: {"model": BadRequestResponse},
        404: {"model": NotFoundResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
def get_all_ongoing_calls():
    calls = call_service.get_ongoing_calls(SQLAlchemyUnitOfWork())

    return GetOngoingCalls(
        data=[
            CallResponseModel(**call_entity.dict()) for call_entity in calls
        ],
    )


@router.get(
    "/{call_id}/details",
    status_code=200,
    responses={
        200: {"model": GetCallDetailsResponse},
        400: {"model": BadRequestResponse},
        404: {"model": NotFoundResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
def get_call_details(call_id: UUID):
    return GetCallDetailsResponse(
        data=[
            CallDetailResponseModel(**call_entity.dict())
            for call_entity in call_service.get_call_details(
                SQLAlchemyUnitOfWork(), call_id
            )
        ],
    )


@router.get(
    "/{call_id}/recordings",
    status_code=200,
    responses={
        200: {"model": GetRecordingsResponse},
        400: {"model": BadRequestResponse},
        404: {"model": NotFoundResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
def get_call_recordings(call_id: UUID):
    return GetRecordingsResponse(
        data=[
            RecordingResponseModel(**recording.dict())
            for recording in call_service.get_recordings(
                SQLAlchemyUnitOfWork(), call_id
            )
        ],
    )
