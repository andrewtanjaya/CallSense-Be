from typing import List, Optional

from sqlalchemy import desc, func

from common.orm import CallSQL
from src.call.domain.entity import Agent
from src.call.domain.interface import AgentAbstractRepository


class AgentSqlAlchemyRepository(AgentAbstractRepository):
    def __init__(self, session) -> None:
        self.session = session

    def get_agents(
        self,
    ) -> List[Agent]:
        query = (
            self.session.query(
                CallSQL.agent_name.label("agent_name"),
                func.count(CallSQL.id).label("total_calls"),
                func.avg(CallSQL.sentiment).label("average_sentiment"),
            )
            .where(CallSQL.ended_at.isnot(None))
            .where(CallSQL.sentiment.isnot(None))
            .group_by(CallSQL.agent_name)
        )

        return [
            self._model_to_entity(agent_name, total_calls, average_sentiment)
            for agent_name, total_calls, average_sentiment in query.all()
        ]

    def _model_to_entity(
        self, agent_name: str, total_calls: int, average_sentiment: float
    ) -> Optional[Agent]:
        if not agent_name:
            return None
        return Agent(
            agent_name=agent_name,
            total_calls=total_calls,
            average_sentiment=average_sentiment,
        )
