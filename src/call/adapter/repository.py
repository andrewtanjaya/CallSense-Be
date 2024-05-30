from typing import List, Optional

from sqlalchemy import desc, func

from common.orm import CallDetailSQL, CallSQl
from src.call.domain.entity import Call, EndedCall
from src.call.domain.interface import CallAbstractRepository


class CallSqlAlchemyRepository(CallAbstractRepository):
    def __init__(self, session) -> None:
        self.session = session

    # def create(self, notification: Notification) -> None:
    #     self.session.add(self._entity_to_model(notification))

    # def bulk_create(self, notifications: List[Notification]) -> None:
    #     self.session.add_all(
    #         [
    #             self._entity_to_model(notification)
    #             for notification in notifications
    #         ]
    #     )

    def get_ended_calls(
        self,
    ) -> List[EndedCall]:
        query = (
            self.session.query(
                CallSQl,
                func.count(CallDetailSQL.id).label("total_calls"),
            )
            .outerjoin(CallDetailSQL, CallSQl.id == CallDetailSQL.call_id)
            .where(CallSQl.ended_at.isnot(None))
            .order_by(desc(CallSQl.created_at))
            .group_by(
                CallSQl.id,
                CallSQl.agent_name,
                CallSQl.sentiment,
                CallSQl.created_at,
                CallSQl.started_at,
                CallSQl.ended_at,
            )
        )

        return [
            self._model_to_ended_entity(call, total_count)
            for call, total_count in query.all()
        ]

    def get_ongoing_calls(
        self,
    ) -> List[Call]:
        return [
            self._model_to_entity(call)
            for call in self.session.query(CallSQl)
            .filter_by(ended_at=None)
            .order_by(desc(CallSQl.created_at))
            .all()
        ]

    def _entity_to_model(self, call: Call) -> CallSQl:
        return CallSQl(**call.dict())

    def _model_to_entity(self, call: CallSQl) -> Optional[Call]:
        if not call:
            return None
        return Call(**call.__dict__)

    def _model_to_ended_entity(
        self, call: CallSQl, total_calls: Optional[int] = None
    ) -> Optional[EndedCall]:
        if not call:
            return None
        return EndedCall(**call.__dict__, total_calls=total_calls)
