from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CallsResponseModel(BaseModel):
    id: UUID
    agent_name: str
    sentiment: float
    started_at: datetime
    ended_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        schema_extra = {
            "example": {
                "id": "51e94932-6f65-4dd2-9687-0584dbc3996c",
                "agent_name": "quota-service",
                "sentiment": "0.9",
                "started_at": "2023-03-17 09:47:38.767317",
                "ended_at": "2023-03-17 10:47:38.767317",
                "created_at": "2023-03-17 10:47:38.767317",
            }
        }


class CallDetailResponseModel(BaseModel):
    id: UUID
    call_id: UUID
    sentiment: float
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        schema_extra = {
            "example": {
                "id": "51e94932-6f65-4dd2-9687-0584dbc3996c",
                "agent_name": "quota-service",
                "sentiment": "0.9",
                "started_at": "2023-03-17 09:47:38.767317",
                "ended_at": "2023-03-17 10:47:38.767317",
                "created_at": "2023-03-17 10:47:38.767317",
            }
        }


class RecordingResponseModel(BaseModel):
    id: UUID
    call_id: UUID
    url: Optional[str]
    created_at: Optional[datetime]

    class Config:
        schema_extra = {
            "example": {
                "id": "51e94932-6f65-4dd2-9687-0584dbc3996c",
                "call_id": "a3164093-aa4a-442b-be7e-9730d2a4924d",
                "url": "http://example.com",
                "created_at": "2023-03-17 10:47:38.767317",
            }
        }
