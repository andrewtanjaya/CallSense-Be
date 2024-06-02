from datetime import datetime
from typing import List
from uuid import UUID

from common.exception import NotFoundError
from src.call.domain.entity import (
    Call,
    CallDetail,
    EndedCall,
    OngoingCall,
    Recording,
)
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
) -> List[OngoingCall]:
    with uow:
        ongoing_calls = uow.call.get_ongoing_calls()

        for call in ongoing_calls:
            call.latest_call_detail = uow.call_detail.get_latest_call_detail(
                call.id
            )

        return ongoing_calls


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


def create_call(uow: AbstractUnitOfWork, call: Call):
    with uow:
        uow.call.create(call)
        uow.commit()


def bulk_create_calls(uow: AbstractUnitOfWork, calls: List[Call]):
    with uow:
        uow.call.bulk_create(calls)
        uow.commit()


def update_call(uow: AbstractUnitOfWork, call: Call):
    with uow:
        uow.call.update(call)
        uow.commit()


def delete_call(uow: AbstractUnitOfWork, id: UUID):
    with uow:
        uow.call.delete(id)
        uow.commit()


def initiate_call(
    uow: AbstractUnitOfWork, agent_name: str, streaming_url: str
):
    with uow:
        # invoke a function to capture the streaming_url then extract it into files
        uow.call.create(
            Call(
                agent_name=agent_name,
                started_at=datetime.utcnow(),
            )
        )
        uow.commit()


def end_call(uow: AbstractUnitOfWork, agent_name: str):
    with uow:
        # trigger combinator recording files then upload to firestore
        latest_call = uow.call.get_latest_ongoing_call(agent_name)
        if not latest_call:
            raise NotFoundError(message="No ongoing call found")

        uow.call.end(latest_call.id)
        uow.commit()
