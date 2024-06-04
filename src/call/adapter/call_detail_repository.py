from typing import List, Optional
from uuid import UUID

from sqlalchemy import desc, update

from common.orm.call_detail import CallDetailSQL
from src.call.domain.entity import CallDetail
from src.call.domain.interface import CallDetailAbstractRepository


class CallDetailSqlAlchemyRepository(CallDetailAbstractRepository):
    def __init__(self, session) -> None:
        self.session = session

    def create(self, call_detail: CallDetail):
        self.session.add(self._entity_to_model(call_detail))

    def update_sentiment(self, id: UUID, sentiment: float):
        self.session.execute(
            update(CallDetailSQL)
            .where(CallDetailSQL.id == id)
            .values(sentiment=sentiment)
        )

    def get_call_details(self, call_id: UUID) -> List[CallDetail]:
        return [
            self._model_to_entity(call)
            for call in self.session.query(CallDetailSQL)
            .filter_by(call_id=call_id)
            .order_by(desc(CallDetailSQL.created_at))
            .all()
        ]

    def get_latest_call_detail(self, call_id: UUID) -> List[CallDetail]:
        query = (
            self.session.query(CallDetailSQL)
            .where(CallDetailSQL.call_id == call_id)
            .order_by(desc(CallDetailSQL.created_at))
            .first()
        )

        if query is not None:
            return self._model_to_latest_call_detail_entity(query)
        else:
            return None

    def _entity_to_model(self, call_detail: CallDetail) -> CallDetailSQL:
        return CallDetailSQL(**call_detail.dict())

    def _model_to_entity(
        self, call_detail: CallDetailSQL
    ) -> Optional[CallDetail]:
        if not call_detail:
            return None
        return CallDetail(**call_detail.__dict__)

    def _model_to_latest_call_detail_entity(
        self, call_detail: CallDetailSQL
    ) -> Optional[CallDetail]:
        if not call_detail:
            return None
        return CallDetail(**call_detail.__dict__)
