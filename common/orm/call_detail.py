from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, Integer
from sqlalchemy.dialects.postgresql import UUID

from common.orm.base import Base


class CallDetailSQL(Base):
    __tablename__ = "call_details"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid4,
    )
    call_id = Column(UUID(as_uuid=True), nullable=False)
    sentiment = Column(Float)
    started_at = Column(Integer)
    ended_at = Column(Integer)
    created_at = Column(DateTime)
