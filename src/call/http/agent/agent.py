from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter

from common.schema.exception.response import (
    BadRequestResponse,
    InternalServerErrorResponse,
    NotFoundResponse,
)
from src.call.adapter.uow import SQLAlchemyUnitOfWork
from src.call.http.agent.schema.response import (
    GetAgents,
    AgentResponseModel
)
from src.call.service import agent as agent_service

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
