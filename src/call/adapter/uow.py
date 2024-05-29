from sqlalchemy.orm import scoped_session

from common.dependencies import DB, get_database
from src.call.adapter.call_detail_repository import (
    CallDetailSqlAlchemyRepository,
)
from src.call.adapter.recording_repository import RecordingSqlAlchemyRepository
from src.call.adapter.repository import CallSqlAlchemyRepository
from src.call.domain.interface import AbstractUnitOfWork


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: DB = get_database()):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory.get_session()
        self.set_repository()
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def set_repository(self):
        self.call = CallSqlAlchemyRepository(self.session)
        self.call_detail = CallDetailSqlAlchemyRepository(self.session)
        self.recording = RecordingSqlAlchemyRepository(self.session)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class SessionUnitOfWork(AbstractUnitOfWork):
    """
    For external usage.
    Session commit/rollback will be handled by caller service
    """

    def __init__(self, session: scoped_session):
        self.session = session
        self.set_repository()

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, *args):
        return super().__exit__()

    def set_repository(self):
        self.call = CallSqlAlchemyRepository(self.session)
        self.call_detail = CallDetailSqlAlchemyRepository(self.session)
        self.recording = RecordingSqlAlchemyRepository(self.session)

    def commit(self):
        pass

    def rollback(self):
        pass
