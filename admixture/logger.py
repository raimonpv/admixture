"""Provides config settings for the logger and a way to load them"""

# Imports: standard library
import os
import sys
import logging.config
from typing import Optional


def load_config(
    log_level: str = "INFO",
    log_dir: Optional[str] = None,
    log_file_basename: Optional[str] = None,
    log_name: Optional[str] = None,
    log_console: bool = True,
):
    log_file = None
    if log_dir is not None:
        os.makedirs(log_dir, exist_ok=True)
        log_file = f"{log_dir}/{log_file_basename}.log"
    logger = logging.getLogger(log_name or __name__)
    try:
        logger_config = _create_logger_config(
            log_level=log_level,
            log_file=log_file,
            log_console=log_console,
        )
        logging.config.dictConfig(logger_config)
        success_msg = (
            "Logging configuration was loaded. "
            f"Log messages can be found at {log_file}."
        )
        logger.info(success_msg)
    except Exception as error:
        logger.error("Failed to load logging config!")
        raise error


def _create_logger_config(
    log_level: str,
    log_file: Optional[str] = None,
    log_console: bool = True,
):
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": (
                    "%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s"
                ),
            },
        },
        "handlers": {},
        "loggers": {"": {"handlers": [], "level": log_level}},
    }
    if log_console:
        console = {
            "level": log_level,
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": sys.stdout,
        }
        config["handlers"]["console"] = console  # type: ignore
        config["loggers"][""]["handlers"].append("console")  # type: ignore
    if log_file is not None:
        file_logger = {
            "level": log_level,
            "class": "logging.FileHandler",
            "formatter": "simple",
            "filename": log_file,
            "mode": "w",
        }
        config["handlers"]["file"] = file_logger  # type: ignore
        config["loggers"][""]["handlers"].append("file")  # type: ignore
    return config
