from typing import Any

from common.schema.base.response import BaseResponse
from src.call.http.chat.schema.model.chat import GetChatbotGeneratedAnswerModel


class GetChatbotGeneratedAnswerResponse(BaseResponse):
    data: GetChatbotGeneratedAnswerModel

    def __init__(self, **data: Any) -> None:
        super().__init__(**data, message="Get chatbot generated answer")

    class Config:
        schema_extra = {
            "example": {
                "message": "Get chatbot generated answer",
                "data": GetChatbotGeneratedAnswerModel.Config.schema_extra.get(
                    "example"
                ),
            }
        }
