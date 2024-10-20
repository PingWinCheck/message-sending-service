import logging


def get_logger(level: int = logging.WARNING):
    logging.basicConfig(format='%(levelname)-8s - [%(asctime)s] - [%(module)s:%(lineno)-3s] - %(message)s',
                        encoding='utf-8',
                        level=level)
    logger = logging.getLogger(__name__)
    return logger
