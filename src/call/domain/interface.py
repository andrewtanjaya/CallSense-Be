from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.call.domain.entity import Call, CallDetail, Recording


class CallAbstractRepository(ABC):
    @abstractmethod
    def get_ended_calls(self) -> List[Call]:
        raise NotImplementedError

    @abstractmethod
    def get_ongoing_calls(self) -> List[Call]:
        raise NotImplementedError


class CallDetailAbstractRepository(ABC):
    @abstractmethod
    def get_call_details(self, call_id: UUID) -> List[CallDetail]:
        raise NotImplementedError


class RecordingAbstractRepository(ABC):
    @abstractmethod
    def get_recordings(self, call_id) -> List[Recording]:
        raise NotImplementedError


class AbstractUnitOfWork(ABC):
    call: CallAbstractRepository
    call_detail: CallDetailAbstractRepository
    recording: RecordingAbstractRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
