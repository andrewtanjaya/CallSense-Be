from typing import Any

from common.schema.base.response import ListDataBaseResponseModel
from src.call.http.agent.schema.model.agent import AgentResponseModel


class GetAgents(ListDataBaseResponseModel):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data, message="Get agents successful")

    class Config:
        schema_extra = {
            "example": {
                "message": "Get agents successful",
                "data": [
                    AgentResponseModel.Config.schema_extra.get("example")
                ],
            }
        }
