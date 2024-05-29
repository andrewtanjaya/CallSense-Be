from fastapi.responses import ORJSONResponse
from fastapi.routing import APIRouter

from src.call.http.api import router as call_router

router = APIRouter(
    default_response_class=ORJSONResponse,
)

router.include_router(call_router)
