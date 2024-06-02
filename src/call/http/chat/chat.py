import logging

from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter

from common.schema.exception.response import (
    BadRequestResponse,
    InternalServerErrorResponse,
    NotFoundResponse,
)
from src.call.http.chat.schema.response import (
    GetChatbotGeneratedAnswerModel,
    GetChatbotGeneratedAnswerResponse,
)
from src.call.service import rag as rag_service

router = APIRouter(
    default_response_class=ORJSONResponse,
    prefix="/chats",
    tags=["chat"],
    redirect_slashes=False,
)


@router.get(
    "/generate",
    status_code=200,
    responses={
        200: {"model": GetChatbotGeneratedAnswerResponse},
        400: {"model": BadRequestResponse},
        404: {"model": NotFoundResponse},
        500: {"model": InternalServerErrorResponse},
    },
)
def sentiment(question: str):
    answer = rag_service.qa.invoke(question)["result"]
    return GetChatbotGeneratedAnswerResponse(
        data=GetChatbotGeneratedAnswerModel(question=question, answer=answer)
    )
