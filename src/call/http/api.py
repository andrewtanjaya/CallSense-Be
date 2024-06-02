from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter

from src.call.http.agent.agent import router as agent_router
from src.call.http.call.call import router as call_router
from src.call.http.chat.chat import router as chat_router

router = APIRouter(default_response_class=ORJSONResponse)

router.include_router(call_router)
router.include_router(agent_router)
router.include_router(chat_router)
