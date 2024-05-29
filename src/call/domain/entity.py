from datetime import datetime
from typing import Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field


class Call(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    agent_name: str
    sentiment: float
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow())


class CallDetail(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    call_id: UUID
    sentiment: float
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow())


class Recording(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    call_id: UUID
    url: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow())
