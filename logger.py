import logging

from config import Config
from logging import StreamHandler
from logging.handlers import RotatingFileHandler


def setup_logging():
    # Set the logging level and format
    logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)

    # Get the root logger
    logger = logging.getLogger()

    # Choose and add the appropriate handler
    if Config.LOG_TYPE == 'rotating':
        handler = RotatingFileHandler(Config.LOG_FILE, maxBytes=Config.LOG_MAX_BYTES, backupCount=Config.LOG_BACKUP_COUNT)
    elif Config.LOG_TYPE == 'file':
        handler = logging.FileHandler(Config.LOG_FILE)
    elif Config.LOG_TYPE == 'console':
        handler = StreamHandler()
    else:
        raise ValueError("Invalid log type specified")

    handler.setFormatter(logging.Formatter(Config.LOG_FORMAT))
    logger.addHandler(handler)

