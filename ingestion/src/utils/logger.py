import sys
from loguru import logger
from ingestion.src.utils.config import settings

logger.remove()
logger.add(
    sys.stdout,
    level=settings.log_level,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module} | {message}",
)