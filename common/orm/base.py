from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# class CallSQl(Base):
#     __tablename__ = "calls"
#     id = Column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         index=True,
#         default=uuid4,
#     )
#     agent_name = Column(String)
#     sentiment = Column(Float)
#     started_at = Column(DateTime)
#     ended_at = Column(DateTime)
#     created_at = Column(DateTime)
#
#
#
# class CallDetailSQL(Base):
#     __tablename__ = "call_details"
#     id = Column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         index=True,
#         default=uuid4,
#     )
#     call_id = Column(UUID(as_uuid=True), nullable=False)
#     sentiment = Column(Float)
#     started_at = Column(DateTime)
#     ended_at = Column(DateTime)
#     created_at = Column(DateTime)
#
#
# class RecordingSQL(Base):
#     __tablename__ = "recordings"
#     id = Column(
#         UUID(as_uuid=True),
#         primary_key=True,
#         index=True,
#         default=uuid4,
#     )
#     call_id = Column(UUID(as_uuid=True), nullable=False)
#     url = Column(String)
#     created_at = Column(DateTime)
