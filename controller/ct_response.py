from redis import Redis
import json
from typing import Any, Dict, Union

from datetime import datetime

from controller.ct_log import get_last_log_message

from model.config_schema import (
    AppConfig,
    REDIS_CLIENT,
    SaveRedisPydantic,
    Evaluation,
    )

from controller.ct_log import log_and_store

def get_redis_field(
    rag_redis_key: str, field_name: str, not_found_message: str
) -> Union[Dict[str, Any], str]:
    """
    Retrieve a specific field from a Redis hash.
    
    Args:
        redis_client (Redis): The Redis client instance.
        redis_key (str): The Redis hash key.
        field_name (str): The field to retrieve.
        not_found_message (str): The message to return if the field is not found.
    
    Returns:
        Union[Dict[str, Any], str]: The value of the field as a dictionary or string,
                                    or the not_found_message if not found.
    """    

    value = REDIS_CLIENT.hget(rag_redis_key, field_name)
    if value is not None:
        try:
            value = value.decode('utf-8')
            value = json.loads(value)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            value = f""
    else:
        value = not_found_message
    return value


def response_controller(rag_redis_key: str) -> Union[Dict[str, Any], str]:
    return get_redis_field(rag_redis_key, 'response', 'No response found.')

def usage_controller(rag_redis_key: str) -> Union[Dict[str, Any], str]:
    return get_redis_field(rag_redis_key, 'usage', 'No usage data found.')

def context_controller(rag_redis_key: str) -> Union[Dict[str, Any], str]:
    return get_redis_field(rag_redis_key, 'context', 'No context data found.')

def detail_controller(rag_redis_key: str) -> Union[Dict[str, Any], str]:
    return get_redis_field(rag_redis_key, 'response_json', 'No data found.')

def message_controller(rag_redis_key: str, ) -> Union[Dict[str, Any], str]:
    return get_redis_field(rag_redis_key, 'messages', 'No message found.')

def file_names_controller(rag_redis_key: str) -> Union[Dict[str, Any], str]:
    return get_redis_field(rag_redis_key, 'file_names', 'No file found.')

def evaluation_controller(rag_redis_key: str, ) -> Union[Dict[str, Any], str]:
    """
    Retrieve evaluation-related fields from Redis.
    
    Args:
        redis_key (str): The Redis key for the evaluation.
    
    Returns:
        Dict[str, Any]: A dictionary containing evaluation and observation fields.
    """
    evaluation = {}
    evaluation['evaluation'] = get_redis_field(rag_redis_key, 'evaluation', 'No evaluation found.')
    evaluation['observation'] = get_redis_field(rag_redis_key, 'observation', 'No obervation found.')
    return evaluation


def responses_by_user(user: str) -> Union[Dict[str, Any], str]:
    """
    Retrieve all response keys for a given user from Redis.
    
    Args:
        user (str): The username.
    
    Returns:
        Union[Dict[str, Any], str]: A list of keys or an error message.
    """
    try:
        keys = REDIS_CLIENT.keys(f"response:{user}:*")
        if not keys:
            return []
        return keys
    except Exception as e:
        return f"Erro ao recuperar respostas: {str(e)}"
    
def status_by_user(user: str) -> Union[Dict[str, Any], str]:
    """
    Retrieve status logs for a user.
    
    Args:
        user (str): The username.
    
    Returns:
        Union[Dict[str, Any], str]: A dictionary mapping status keys to log messages or an error message.
    """
    try:
        keys = REDIS_CLIENT.keys(f"status:{user}:*")
        
        if not keys:
            return []
        
        status_dict = {}
        for redis_key_status in keys:
            last_status = get_last_log_message(redis_key_status)
            status_dict[redis_key_status] = last_status

        return status_dict
    
    except Exception as e:
        return f"Erro ao recuperar respostas: {str(e)}"
    

def save_response_to_redis(config: AppConfig, data_to_save: SaveRedisPydantic) -> str:
    """
    Save a response to Redis using a hash key.
    
    Args:
        config (AppConfig): Application configuration.
        data_to_save (SaveRedisPydantic): The data to save.
    
    Returns:
        str: The Redis key used for saving.
    """
    redis_key = f"response:{config.user}:{config.task_id}:{config.type_of_analysis}"
    data_to_save = data_to_save.model_dump()
    print(f'data_to_save:  {data_to_save}')

    try:
        REDIS_CLIENT.hset(redis_key, mapping=data_to_save)
        log_and_store(f"Concluded at", config)
        return redis_key
    except Exception as e:
        log_and_store(f"Error to save on Redis at", config)
        raise

def evaluation_response(rag_redis_key: str, evaluations_items: Evaluation):
    """
    Save evaluation data to Redis.
    
    Args:
        redis_key (str): The Redis key.
        evaluations_items (Evaluation): The evaluation data.
    
    Returns:
        str: The Redis key used for saving.
    """
    evaluations_dict = evaluations_items.model_dump()
    try:
        serialized_evaluations = {k: json.dumps(v) for k, v in evaluations_dict.items()}
        REDIS_CLIENT.hset(rag_redis_key, mapping=serialized_evaluations)
        # log_and_store(f"Concluded and Evalutade at", rag_redis_key)
        return rag_redis_key
    except Exception as e:
        # log_and_store(f"Error to save the evaluation at", rag_redis_key)
        raise