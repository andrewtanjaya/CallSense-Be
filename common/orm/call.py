from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID

from common.orm.base import Base


class CallSQl(Base):
    __tablename__ = "calls"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid4,
    )
    agent_name = Column(String)
    sentiment = Column(Float)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    created_at = Column(DateTime)
