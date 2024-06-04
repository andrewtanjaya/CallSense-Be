from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.call.domain.entity import (
    Agent,
    Call,
    CallDetail,
    EndedCall,
    OngoingCall,
    Recording,
)


class CallAbstractRepository(ABC):
    @abstractmethod
    def get_ended_calls(
        self, agent_name: Optional[str] = None
    ) -> List[EndedCall]:
        raise NotImplementedError

    @abstractmethod
    def get_ongoing_calls(self) -> List[OngoingCall]:
        raise NotImplementedError

    @abstractmethod
    def get_latest_ongoing_call(self, agent_name: str) -> Call:
        raise NotImplementedError

    @abstractmethod
    def create(self, call: Call) -> None:
        raise NotImplementedError

    @abstractmethod
    def bulk_create(self, calls: List[Call]) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, call: Call) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def end(self, id: UUID) -> None:
        raise NotImplementedError


class CallDetailAbstractRepository(ABC):
    @abstractmethod
    def create(self, call_detail: CallDetail) -> CallDetail:
        raise NotImplementedError

    @abstractmethod
    def update_sentiment(self, id: UUID, sentiment: float) -> CallDetail:
        raise NotImplementedError

    @abstractmethod
    def get_call_details(self, call_id: UUID) -> List[CallDetail]:
        raise NotImplementedError

    @abstractmethod
    def get_latest_call_detail(self, call_id: UUID) -> Call:
        raise NotImplementedError


class RecordingAbstractRepository(ABC):
    @abstractmethod
    def get_recordings(self, call_id) -> List[Recording]:
        raise NotImplementedError

    @abstractmethod
    def create(self, recording: Recording) -> Recording:
        raise NotImplementedError

    @abstractmethod
    def get_one_recording(self, call_id: UUID) -> Optional[Recording]:
        raise NotImplementedError


class AgentAbstractRepository(ABC):
    @abstractmethod
    def get_agents(self) -> List[Agent]:
        raise NotImplementedError


class FireStoreAbstractExternal(ABC):
    @abstractmethod
    def get_collections(self):
        raise NotImplementedError


class FireStorageAbstractExternal(ABC):
    @abstractmethod
    def upload(self, file_name: str):
        raise NotImplementedError


class AbstractUnitOfWork(ABC):
    call: CallAbstractRepository
    call_detail: CallDetailAbstractRepository
    recording: RecordingAbstractRepository
    firestore: FireStoreAbstractExternal
    firestorage: FireStorageAbstractExternal
    agent: AgentAbstractRepository

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
