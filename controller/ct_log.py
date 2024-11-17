import logging
from redis import Redis

from model.config_schema import AppConfig, REDIS_CLIENT

from datetime import datetime

# Configurar o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_and_store(message: str, config: AppConfig):
    redis_key_status = f"status:{config.user}:{config.task_id}:{config.type_of_analysis}"
    timestamp = datetime.now().isoformat()
    logger.info(message)
    REDIS_CLIENT.rpush(redis_key_status, f"{message} às {timestamp}")

def get_last_log_message(redis_key_status: str):
    last_message = REDIS_CLIENT.lindex(redis_key_status, -1)
    return last_message
