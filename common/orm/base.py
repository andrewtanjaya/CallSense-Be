from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
