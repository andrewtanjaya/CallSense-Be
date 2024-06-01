from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from src.call.http.call.schema.response import EndedCallResponseModel


class AgentEndedCallResponseModel(BaseModel):
    id: UUID
    sentiment: float
    started_at: datetime
    ended_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": "7c9afc72-e9a7-4d1c-9cee-9a0ad0066b30",
                "sentiment": "0.9",
                "started_at": "2023-03-17 10:47:38.767317",
                "ended_at": "2023-03-17 10:47:38.767317",
            }
        }


class AgentResponseModel(BaseModel):
    agent_name: str
    total_calls: int
    average_sentiment: float
    calls: Optional[List[AgentEndedCallResponseModel]]

    class Config:
        schema_extra = {
            "example": {
                "agent_name": "Agent 2",
                "total_calls": "5",
                "average_sentiment": "0.9",
                "calls": [
                    AgentEndedCallResponseModel.Config.schema_extra.get("example")
                ],
            }
        }

