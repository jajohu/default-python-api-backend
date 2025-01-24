import logging
from typing import Dict
from fastapi import FastAPI
from app.routes import router

logging.basicConfig(
    filename="/app/logs/app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Orbital Witness Usage API",
    description="An API service to retrieve service usage over a billing period",
    version="1.0.0",
)

app.include_router(router)


@app.get("/health")
async def health_check() -> Dict[str, str]:
    logger.debug("Health check received")
    return {"status": "healthy"}
