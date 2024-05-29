from typing import List, Optional
from uuid import UUID

from sqlalchemy import desc

from common.orm.recording import RecordingSQL
from src.call.domain.entity import Recording
from src.call.domain.interface import RecordingAbstractRepository


class RecordingSqlAlchemyRepository(RecordingAbstractRepository):
    def __init__(self, session) -> None:
        self.session = session

    def get_recordings(self, call_id: UUID) -> List[Recording]:
        return [
            self._model_to_entity(recording)
            for recording in self.session.query(RecordingSQL)
            .filter_by(call_id=call_id)
            .order_by(desc(RecordingSQL.created_at))
            .all()
        ]

    def _entity_to_model(self, recording: Recording) -> RecordingSQL:
        return RecordingSQL(**recording.dict())

    def _model_to_entity(self, recording: RecordingSQL) -> Optional[Recording]:
        if not recording:
            return None
        return Recording(**recording.__dict__)
