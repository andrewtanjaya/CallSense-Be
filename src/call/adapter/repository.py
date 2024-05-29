from typing import List, Optional

from sqlalchemy import desc

from common.orm.call import CallSQl
from src.call.domain.entity import Call
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
    ) -> List[Call]:
        return [
            self._model_to_entity(call)
            for call in self.session.query(CallSQl)
            .filter(CallSQl.ended_at.isnot(None))
            .order_by(desc(CallSQl.created_at))
            .all()
        ]

    # query = (
    #     select([
    #         call.c.id,
    #         call.c.agent_name,
    #         call.c.sentiment,
    #         call.c.created_at,
    #         call.c.started_at,
    #         call.c.ended_at,
    #         func.count(call_detail.c.id).label('call_detail_count')
    #     ])
    #     .select_from(call.outerjoin(call_detail, call.c.id == call_detail.c.call_id))
    #     .group_by(call.c.id)
    # )

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
