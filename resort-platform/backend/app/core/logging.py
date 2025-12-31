import logging
import sys
from typing import Optional

from loguru import logger

# -------------------------------------------------
# Configuration
# -------------------------------------------------

LOG_LEVEL = logging.INFO
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)


# -------------------------------------------------
# Intercept standard logging
# -------------------------------------------------

class InterceptHandler(logging.Handler):
    """
    Redirects standard logging (logging module)
    to Loguru.
    """

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(
            depth=depth,
            exception=record.exc_info,
        ).log(level, record.getMessage())


# -------------------------------------------------
# Setup function
# -------------------------------------------------

def setup_logging(
    level: Optional[int] = None,
) -> None:
    """
    Configure Loguru and intercept standard logging.

    Call this once at application startup.
    """

    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(level or LOG_LEVEL)

    for logger_name in (
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "sqlalchemy.engine",
        "sqlalchemy.pool",
    ):
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = []
        logging_logger.propagate = True

    logger.remove()
    logger.add(
        sys.stdout,
        level=level or LOG_LEVEL,
        format=LOG_FORMAT,
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )
