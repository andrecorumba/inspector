import logging
from redis import Redis

from model.config_schema import AppConfig, REDIS_CLIENT

from datetime import datetime

# Configurar o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_and_store(message: str, config: AppConfig):
    """
    Logs a message and stores it in a Redis list with a timestamp.

    Args:
        message (str): The message to be logged and stored.
        config (AppConfig): An application configuration object containing user, task, and analysis details.

    Returns:
        None
    """
    
    redis_key_status = f"status:{config.user}:{config.task_id}:{config.type_of_analysis}"
    timestamp = datetime.now().isoformat()
    logger.info(message)
    REDIS_CLIENT.rpush(redis_key_status, f"{message} at {timestamp}")

def get_last_log_message(redis_key_status: str):
    """
    Retrieves the last log message from a Redis list.

    Args:
        redis_key_status (str): The Redis key pointing to the list of log messages.

    Returns:
        str or None: The last message in the Redis list, or None if the list is empty.
    """

    last_message = REDIS_CLIENT.lindex(redis_key_status, -1)
    return last_message
