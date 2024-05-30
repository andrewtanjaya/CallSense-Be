from typing import List
from uuid import UUID

from src.call.domain.entity import Call, CallDetail, EndedCall, Recording
from src.call.domain.interface import AbstractUnitOfWork


def get_ended_calls(
    uow: AbstractUnitOfWork,
) -> List[EndedCall]:
    with uow:
        ended_calls = uow.call.get_ended_calls()
        for call in ended_calls:
            call.details = uow.call_detail.get_call_details(call.id)

        return ended_calls


def get_ongoing_calls(
    uow: AbstractUnitOfWork,
) -> List[Call]:
    with uow:
        return uow.call.get_ongoing_calls()


def get_recordings(uow: AbstractUnitOfWork, call_id: UUID) -> List[Recording]:
    with uow:
        return uow.recording.get_recordings(call_id=call_id)


def get_call_details(
    uow: AbstractUnitOfWork, call_id: UUID
) -> List[CallDetail]:
    with uow:
        return uow.call_detail.get_call_details(call_id=call_id)


def get_firestore_collections(uow: AbstractUnitOfWork):
    with uow:
        return uow.firestore.get_collections()


def upload_file_to_firestorage(uow: AbstractUnitOfWork, file_name: str):
    with uow:
        return uow.firestorage.upload(file_name)
