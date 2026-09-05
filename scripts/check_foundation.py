from doc_intel_agent.core.config import get_settings
from doc_intel_agent.core.logging import configure_logging, get_logger

settings = get_settings()
configure_logging(settings)
log = get_logger(__name__)

log.info("startup", environment=settings.environment, qdrant_url=settings.qdrant.url)