from fastapi import BackgroundTasks
from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter

from common.schema.base.response import CreatedResponse, SuccessResponse
from common.schema.exception.response import (
    BadRequestResponse,
    InternalServerErrorResponse,
    NotFoundResponse,
)
from src.call.adapter.uow import SQLAlchemyUnitOfWork
from src.call.http.agent.schema import (
    AgentResponseModel,
    GetAgents,
    InitiateCallRequest,
)
from src.call.service import agent as agent_service
from src.call.service import call as call_service
from src.call.service import recording as recording_service

router = APIRouter(
    default_response_class=ORJSONResponse,
    prefix="/agents",
    tags=["agents"],
    redirect_slashes=False,
)


@router.get(
    "",
    status_code=200,
    responses={
        200: {"model": GetAgents},
        400: {"model": BadRequestResponse},
        404: {"model": NotFoundResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
def get_all_agents():
    agents = agent_service.get_agents(SQLAlchemyUnitOfWork())

    return GetAgents(
        data=[
            AgentResponseModel(**agent_entity.dict())
            for agent_entity in agents
        ],
    )


@router.post(
    "/{agent_name}/calls/start",
    status_code=201,
    responses={
        201: {"model": CreatedResponse},
        400: {"model": BadRequestResponse},
        404: {"model": NotFoundResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
def start_call(
    agent_name: str,
    request: InitiateCallRequest,
    background_tasks: BackgroundTasks,
):
    call_service.initiate_call(
        SQLAlchemyUnitOfWork(), agent_name, request.customer_streaming_url
    )
    background_tasks.add_task(
        recording_service.stream_audio_and_save_in_chunks,
        SQLAlchemyUnitOfWork(),
        request.customer_streaming_url,
        "mp3",
        "wav",
        10,
    )
    return CreatedResponse(message="Call initiated successfully")


@router.put(
    "/{agent_name}/calls/ends",
    status_code=204,
    responses={
        200: {"model": SuccessResponse},
        400: {"model": BadRequestResponse},
        404: {"model": NotFoundResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
def end_call(agent_name: str):
    call_service.end_call(SQLAlchemyUnitOfWork(), agent_name)
    return SuccessResponse(message="Latest ongoing call ended successfully")
