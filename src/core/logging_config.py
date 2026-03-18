import structlog
import logging
import sys

def configure_logging():
    """
    Configure structured logging for the application.
    """
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    structlog.configure(
        processors=shared_processors + [
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard logging to use structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    # Redirect standard logging to structlog
    def redirect_logging(logger_name, level, event_dict):
        event_dict["logger"] = logger_name
        return event_dict

configure_logging()
logger = structlog.get_logger()
