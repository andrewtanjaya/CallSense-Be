from typing import List

from src.call.domain.entity import Agent
from src.call.domain.interface import AbstractUnitOfWork


def get_agents(
    uow: AbstractUnitOfWork,
) -> List[Agent]:
    with uow:
        agents = uow.agent.get_agents()
        for agent in agents:
            calls = uow.call.get_ended_calls(agent.agent_name)
            for call in calls:
                call.sentiment *= 100
            agent.calls = calls

        return agents
