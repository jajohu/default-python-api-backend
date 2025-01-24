import logging
from fastapi import APIRouter

from app.models.usage import Usage
from app.services import get_usage


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/usage")
async def get_questionnaire_route() -> Usage:
    """Get credit usage over the current billing period."""
    logger.debug("Received usage request")
    return get_usage()