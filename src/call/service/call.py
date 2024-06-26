from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

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


def get_agent_ended_calls(
    uow: AbstractUnitOfWork, agent_name: str
) -> List[EndedCall]:
    with uow:
        ended_calls = uow.call.get_ended_calls(agent_name)
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


def get_one_recording(
    uow: AbstractUnitOfWork, call_id: UUID
) -> Optional[Recording]:
    with uow:
        recording = uow.recording.get_one_recording(call_id=call_id)
        # if recording:
        #     recording.url = uow.firestorage.get_storage_url(recording.url)
        return recording


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
    uow: AbstractUnitOfWork,
    agent_name: str,
    customer_streaming_url: str,
    agent_streaming_url: str,
) -> UUID:
    with uow:
        new_call = Call(
            id=uuid4(),
            agent_name=agent_name,
            started_at=datetime.utcnow(),
            customer_streaming_url=customer_streaming_url,
            agent_streaming_url=agent_streaming_url,
        )
        uow.call.create(new_call)
        uow.commit()

    return new_call.id


def end_call(uow: AbstractUnitOfWork, agent_name: str):
    with uow:
        # calculate the sentiment based on call detail
        latest_call = uow.call.get_latest_ongoing_call(agent_name)
        if not latest_call:
            raise NotFoundError(message="No ongoing call found")

        call_details = uow.call_detail.get_call_details(latest_call.id)

        total_value = 0
        total_ended_at = 0
        for call_detail in call_details:
            if call_detail.sentiment > 0.3:
                value = call_detail.ended_at
            elif call_detail.sentiment <= 0.3:
                value = call_detail.ended_at * -1
            else:
                value = 0
            total_value += value
            total_ended_at += call_detail.ended_at

        result = total_value / total_ended_at

        latest_call.ended_at = datetime.utcnow()
        latest_call.sentiment = result
        uow.call.update(latest_call)
        uow.commit()
