from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel
from src.call.http.call.schema.response import EndedCallResponseModel


class AgentResponseModel(BaseModel):
    agent_name: str
    total_calls: int
    average_sentiment: float
    calls: Optional[List[EndedCallResponseModel]]

    class Config:
        schema_extra = {
            "example": {
                "agent_name": "Agent 2",
                "total_calls": "5",
                "average_sentiment": "0.9",
                "calls": [
                    EndedCallResponseModel.Config.schema_extra.get("example")
                ]
            }
        }
