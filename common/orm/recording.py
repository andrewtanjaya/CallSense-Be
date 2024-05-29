from uuid import uuid4

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from common.orm.base import Base


class RecordingSQL(Base):
    __tablename__ = "recordings"
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid4,
    )
    call_id = Column(UUID(as_uuid=True), nullable=False)
    url = Column(String)
    created_at = Column(DateTime)
