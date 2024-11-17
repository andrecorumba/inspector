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
    # rag_redis_key = f"rag:{config.user}:{config.task_id}:{config.type_of_analysis}"
    value = REDIS_CLIENT.hget(rag_redis_key, field_name)
    if value is not None:
        try:
            value = value.decode('utf-8')
            value = json.loads(value)
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            # value = f"Erro ao decodificar ou analisar o JSON: {str(e)}"
            value = f""
    else:
        value = not_found_message
    return value


def response_controller(rag_redis_key: str) -> Union[Dict[str, Any], str]:
    return get_redis_field(rag_redis_key, 'response', 'Nenhuma resposta encontrada.')


def usage_controller(rag_redis_key: str) -> Union[Dict[str, Any], str]:
    return get_redis_field(rag_redis_key, 'usage', 'Nenhum dado de uso encontrado.')


def context_controller(rag_redis_key: str) -> Union[Dict[str, Any], str]:
    return get_redis_field(rag_redis_key, 'context', 'Nenhum dado de uso encontrado.')

def detail_controller(rag_redis_key: str) -> Union[Dict[str, Any], str]:
    return get_redis_field(rag_redis_key, 'response_json', 'Nenhum dado de uso encontrado.')

def message_controller(rag_redis_key: str, ) -> Union[Dict[str, Any], str]:
    return get_redis_field(rag_redis_key, 'messages', 'Nenhum dado de uso encontrado.')

def file_names_controller(rag_redis_key: str) -> Union[Dict[str, Any], str]:
    return get_redis_field(rag_redis_key, 'file_names', 'Nenhum dado de uso encontrado.')

def evaluation_controller(rag_redis_key: str, ) -> Union[Dict[str, Any], str]:
    evaluation = {}
    evaluation['evaluation'] = get_redis_field(rag_redis_key, 'evaluation', 'Nenhum dado de avaliação encontrado.')
    evaluation['observation'] = get_redis_field(rag_redis_key, 'observation', 'Nenhum dado de observação encontrado.')
    return evaluation


def responses_by_user(user: str) -> Union[Dict[str, Any], str]:
    try:
        keys = REDIS_CLIENT.keys(f"response:{user}:*")
        if not keys:
            return []
        return keys
    except Exception as e:
        return f"Erro ao recuperar respostas: {str(e)}"
    
def status_by_user(user: str) -> Union[Dict[str, Any], str]:
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
    """Salva os dados do objeto SaveRedisPydantic no Redis usando uma única chave de hash."""
    redis_key = f"response:{config.user}:{config.task_id}:{config.type_of_analysis}"
    data_to_save = data_to_save.model_dump()
    print(f'data_to_save:  {data_to_save}')
    
    #data_to_save_dict = {k: (v if v is not None else "") for k, v in data_to_save.items()}
   

    try:
        REDIS_CLIENT.hset(redis_key, mapping=data_to_save)
        log_and_store(f"Concluido", config)
        return redis_key
    except Exception as e:
        log_and_store(f"Erro ao salvar no Redis", config)
        raise

def evaluation_response(rag_redis_key: str, evaluations_items: Evaluation):
    """Avalia as respostas."""
    # redis_key = f"response:{config.user}:{config.task_id}:{config.type_of_analysis}"
    evaluations_dict = evaluations_items.model_dump()
    # Serializa evaluations_dict em JSON antes de salvar
    try:
        serialized_evaluations = {k: json.dumps(v) for k, v in evaluations_dict.items()}
        REDIS_CLIENT.hset(rag_redis_key, mapping=serialized_evaluations)
        # log_and_store(f"Concluido e Avaliado", rag_redis_key)
        return rag_redis_key
    except Exception as e:
        # log_and_store(f"Erro ao salvar avaliação", rag_redis_key)
        raise