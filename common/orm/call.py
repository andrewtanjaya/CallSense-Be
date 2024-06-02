from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID

from common.orm.base import Base


class CallSQL(Base):
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
    customer_streaming_url = Column(String)
    agent_streaming_url = Column(String)
    created_at = Column(DateTime)
