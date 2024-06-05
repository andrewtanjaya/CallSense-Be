from datetime import datetime
from typing import Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class Call(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    agent_name: str
    sentiment: Optional[float] = 0.0
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    customer_streaming_url: Optional[str]
    agent_streaming_url: Optional[str]


class CallDetail(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    call_id: UUID
    sentiment: Optional[float] = 0.0
    started_at: Optional[int]
    ended_at: Optional[int]
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class EndedCall(Call):
    total_calls: int
    details: Optional[List[CallDetail]]


class OngoingCall(Call):
    latest_call_detail: Optional[CallDetail]


class Recording(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    call_id: UUID
    url: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class Agent(BaseModel):
    agent_name: str
    total_calls: int
    average_sentiment: float
    calls: Optional[List[Call]]
