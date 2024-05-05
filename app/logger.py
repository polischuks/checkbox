import logging


def get_logger():
    logger = logging.getLogger("uvicorn.error")
    return logger
