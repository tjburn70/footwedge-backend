import logging


def get_logger(name: str, log_level: str = logging.INFO):
    logger = logging.getLogger(name=name)
    logger.setLevel(level=log_level)
    return logger
