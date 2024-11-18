from typing import Any
from redis import Redis

from datetime import datetime

from model.embedding import InspectorEmbeddings
from model.tika import TikaParser
from model.vector_redis import RedisVectorStore
from model.config_schema import AppConfig

from controller.ct_log import log_and_store

from model.config_schema import (
    AppConfig, 
    REDIS_CLIENT,
    TIKA_SERVER_ENDPOINT
    )


def upload_controller(file_bytes: bytes, file_name: str, config: AppConfig) -> Any:
    """
    Processa o arquivo enviado, extrai o conteúdo usando o parser Tika, cria embeddings,
    armazena os dados no Redis e carrega os embeddings no armazenamento de vetores Redis.
    """

    sufix = f"{config.user}:{config.task_id}:{config.type_of_analysis}"
    redis_key_status = f"status:{config.user}:{config.task_id}:{config.type_of_analysis}"

    try:
        # Analisar o conteúdo do arquivo usando o Tika
        tika_parser = TikaParser(tika_server=TIKA_SERVER_ENDPOINT)
        content = tika_parser.tika_parser_from_bytes(file_bytes)
        file_hash = tika_parser.hash_file_bytes(file_bytes)
        
        # Pega apensa as 16 primeiras posições do hash
        redis_key_file = f"file:{sufix}:{file_hash[:16]}"
        
        log_and_store(f"Tika: Extraído arquivo {file_name}", config)

        if content is None:
            log_and_store(f"Tika: Erro ao extrair arquivo {file_name}", config)
            return

        # Armazenar o conteúdo analisado no Redis
        REDIS_CLIENT.hset(redis_key_file, mapping={
            'file_name': file_name,
            'file': content,
            'tokenized': '',
            })
        log_and_store(f"Tika: Arquivo salvo: '{redis_key_file}", config)
        
        return redis_key_file

    except Exception as e:
        log_and_store(f"Tika: Erro em upload_controller: {e}", config)
        raise