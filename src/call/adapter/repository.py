from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import desc, func, update

from common.orm import CallDetailSQL, CallSQL
from src.call.domain.entity import Call, EndedCall
from src.call.domain.interface import CallAbstractRepository


class CallSqlAlchemyRepository(CallAbstractRepository):
    def __init__(self, session) -> None:
        self.session = session

    def create(self, call: Call) -> None:
        self.session.add(self._entity_to_model(call))

    def bulk_create(self, calls: List[Call]) -> None:
        self.session.add_all([self._entity_to_model(call) for call in calls])

    def update(self, call: Call) -> None:
        self.session.execute(
            update(CallSQL)
            .where(CallSQL.id == call.id)
            .values(call.dict(exclude={"id"}))
        )

    def end(self, id: UUID) -> None:
        self.session.execute(
            update(CallSQL)
            .where(CallSQL.id == id)
            .values(
                ended_at=datetime.utcnow(),
            )
        )

    def delete(self, id: UUID) -> None:
        self.session.query(CallSQL).filter_by(id=id).delete()

    def get_ended_calls(
        self, agent_name: Optional[str] = None
    ) -> List[EndedCall]:
        query = (
            self.session.query(
                CallSQL,
                func.count(CallDetailSQL.id).label("total_calls"),
            )
            .outerjoin(CallDetailSQL, CallSQL.id == CallDetailSQL.call_id)
            .where(CallSQL.ended_at.isnot(None))
            .order_by(desc(CallSQL.created_at))
            .group_by(
                CallSQL.id,
                CallSQL.agent_name,
                CallSQL.sentiment,
                CallSQL.created_at,
                CallSQL.started_at,
                CallSQL.ended_at,
            )
        )

        if agent_name:
            query = query.where(CallSQL.agent_name == agent_name)

        return [
            self._model_to_ended_entity(call, total_count)
            for call, total_count in query.all()
        ]

    def get_ongoing_calls(
        self,
    ) -> List[Call]:
        return [
            self._model_to_entity(call)
            for call in self.session.query(CallSQL)
            .filter_by(ended_at=None)
            .order_by(desc(CallSQL.created_at))
            .all()
        ]

    def get_latest_ongoing_call(self, agent_name: str) -> Optional[Call]:
        call = (
            self.session.query(CallSQL)
            .filter_by(ended_at=None, agent_name=agent_name)
            .order_by(desc(CallSQL.created_at))
            .first()
        )
        return self._model_to_entity(call)

    def _entity_to_model(self, call: Call) -> CallSQL:
        return CallSQL(**call.dict())

    def _model_to_entity(self, call: CallSQL) -> Optional[Call]:
        if not call:
            return None
        return Call(**call.__dict__)

    def _model_to_ended_entity(
        self, call: CallSQL, total_calls: Optional[int] = None
    ) -> Optional[EndedCall]:
        if not call:
            return None
        return EndedCall(**call.__dict__, total_calls=total_calls)
