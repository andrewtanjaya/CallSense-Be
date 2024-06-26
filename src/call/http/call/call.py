import logging
from uuid import UUID

from fastapi import BackgroundTasks
from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter

from common.schema.base.response import SuccessResponse
from common.schema.exception.response import (
    BadRequestResponse,
    InternalServerErrorResponse,
    NotFoundResponse,
)
from src.call.adapter.uow import SQLAlchemyUnitOfWork
from src.call.http.call.schema.request import CallDetailSentimentRequest
from src.call.http.call.schema.response import (
    CallDetailResponseModel,
    CallResponseModel,
    EndedCallResponseModel,
    GetCallDetailsResponse,
    GetEndedCalls,
    GetOngoingCalls,
    GetRecordingsResponse,
    GetSentimentCallResponse,
    OngoingCallResponseModel,
    RecordingResponseModel,
)
from src.call.service import call as call_service
from src.call.service import recording as recording_service
from src.call.service import sentiment as sentiment_service

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
    deprecated=True,
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
            OngoingCallResponseModel(**call_entity.dict())
            for call_entity in calls
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
def get_call_recording(call_id: UUID):
    recording = call_service.get_one_recording(SQLAlchemyUnitOfWork(), call_id)

    call_detail_models = []
    if recording is not None:
        call_details = call_service.get_call_details(
            SQLAlchemyUnitOfWork(), recording.call_id
        )
        call_detail_models = [
            CallDetailResponseModel(
                **call_detail.dict(exclude={"sentiment"}),
                sentiment=call_detail.sentiment * 100
            )
            for call_detail in call_details
        ]
    # responses_data.append(
    #     RecordingResponseModel(
    #         **recording.dict(), details=call_detail_models
    #     )
    # )

    return GetRecordingsResponse(
        data=RecordingResponseModel(
            **recording.dict(), details=call_detail_models
        )
    )


@router.get(
    "/upload",
    status_code=200,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": BadRequestResponse},
        404: {"model": NotFoundResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
def get_firestore_collections():
    call_service.upload_file_to_firestorage(
        SQLAlchemyUnitOfWork(), "ganteng.png"
    )
    return SuccessResponse(message="File uploaded successfully")


@router.delete(
    "/{call_id}",
    status_code=204,
    responses={
        400: {"model": BadRequestResponse},
        404: {"model": NotFoundResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
def delete_call(call_id: UUID):
    call_service.delete_call(SQLAlchemyUnitOfWork(), call_id)


@router.post(
    "/{call_detail_id}/sentiment",
    status_code=200,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": BadRequestResponse},
        404: {"model": NotFoundResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
def sentiment(
    call_detail_id: UUID,
    request: CallDetailSentimentRequest,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(
        sentiment_service.predict_emotion,
        SQLAlchemyUnitOfWork(),
        request.file_path,
        call_detail_id,
    )
    # logging.info(f"category:{category}, confidence:{confidence}")
    return SuccessResponse(message="AI Sentiment called successfully")
    # return GetSentimentCallResponse(
    #     category=category, confidence=confidence * 100
    # )


@router.post(
    "/{call_id}/recordings",
    status_code=200,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": BadRequestResponse},
        404: {"model": NotFoundResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
def create_recordings(
    call_id: UUID,
):
    recording_service.create_recording(
        SQLAlchemyUnitOfWork(),
        call_id,
        "https://google.com/",
    )
    return SuccessResponse(message="AI Sentiment called successfully")
