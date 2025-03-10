import uuid
import logging


def generate_uuid():
    """
    Generate a unique UUID for database records
    """
    return str(uuid.uuid4())


def get_logger(name):
    """
    Get a configured logger with consistent formatting
    """
    logger = logging.getLogger(f"bookmark-api.{name}")
    return logger
