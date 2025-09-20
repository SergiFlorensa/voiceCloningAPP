from __future__ import annotations

import logging
from logging.config import dictConfig

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def configure_logging(level: str = "INFO") -> None:
    """Apply a basic logging configuration."""
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": LOG_FORMAT,
                }
            },
            "handlers": {
                "default": {
                    "level": level,
                    "formatter": "standard",
                    "class": "logging.StreamHandler",
                }
            },
            "root": {
                "handlers": ["default"],
                "level": level,
            },
        }
    )


__all__ = ["configure_logging"]
