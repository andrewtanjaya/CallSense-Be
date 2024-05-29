from typing import List, Optional
from uuid import UUID

from sqlalchemy import desc

from common.orm.call_detail import CallDetailSQL
from src.call.domain.entity import CallDetail
from src.call.domain.interface import CallDetailAbstractRepository


class CallDetailSqlAlchemyRepository(CallDetailAbstractRepository):
    def __init__(self, session) -> None:
        self.session = session

    def get_call_details(self, call_id: UUID) -> List[CallDetail]:
        return [
            self._model_to_entity(call)
            for call in self.session.query(CallDetailSQL)
            .filter_by(call_id=call_id)
            .order_by(desc(CallDetailSQL.created_at))
            .all()
        ]

    def _entity_to_model(self, call_detail: CallDetail) -> CallDetailSQL:
        return CallDetailSQL(**call_detail.dict())

    def _model_to_entity(
        self, call_detail: CallDetailSQL
    ) -> Optional[CallDetail]:
        if not call_detail:
            return None
        return CallDetail(**call_detail.__dict__)
