"""
FastAPI entrypoint.

Run with: uvicorn doc_intel_agent.api.main:app --reload
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from doc_intel_agent.api.schemas import HealthResponse
from doc_intel_agent.core.config import get_settings
from doc_intel_agent.core.logging import configure_logging, get_logger

settings = get_settings()
configure_logging(settings)
log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("api_startup", environment=settings.environment, port=settings.api.port)
    yield
    log.info("api_shutdown")


app = FastAPI(title="doc-intel-agent", version="0.1.0", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(environment=settings.environment.value)
