import logging
from typing import Dict
from fastapi import FastAPI
from fastapi import APIRouter

logging.basicConfig(
    filename="/app/logs/app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Basic Python API",
    description="A basic Python API implemented in FastAPI",
    version="1.0.0",
)
router = APIRouter()

app.include_router(router)


@app.get("/health")
async def health_check() -> Dict[str, str]:
    logger.debug("Health check received")
    return {"status": "ok"}
