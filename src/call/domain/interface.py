from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.call.domain.entity import Call, CallDetail, EndedCall, Recording, Agent

class CallAbstractRepository(ABC):
    @abstractmethod
    def get_ended_calls(self, agent_name: Optional[str] = None) -> List[EndedCall]:
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
