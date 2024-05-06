import logging


def get_logger() -> logging.Logger:
    logger = logging.getLogger("uvicorn.error")
    return logger
