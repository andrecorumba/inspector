import json
import logging
from redis import Redis
from typing import Any

from datetime import datetime

from model.config_schema import AppConfig, SaveRedisPydantic
from model.rag import RAGRedis
from model.embedding import Embeddings
from model.vector_redis import RedisVectorStore

from controller.ct_log import log_and_store
from controller import ct_response

def save_rag_redis(config: AppConfig, rag_obj: RAGRedis, redis_client: Redis) -> str:
    """Salva os dados do objeto RAGRedis no Redis usando uma única chave de hash."""
    try:
        redis_key = f"rag:{config.user}:{config.task_id}:{config.type_of_analysis}"
        redis_key_status = f"status:{config.user}:{config.task_id}:{config.type_of_analysis}"

        # Serializar os dados para JSON
        data_to_save = {
            'response': json.dumps(rag_obj.response),
            'context': json.dumps(rag_obj.context),
            'usage': json.dumps(rag_obj.usage),
            'response_json': json.dumps(rag_obj.response_json),
            'messages': json.dumps(rag_obj.messages),
            'type_of_analysis': json.dumps(config.type_of_analysis),
        }

        # Armazenar todos os dados sob uma única chave de hash
        redis_client.hset(redis_key, mapping=data_to_save)
        log_and_store(f"Concluded at", config)
        return redis_key
    except Exception as e:
        # logging.error(f"Ocorreu um erro ao salvar no Redis: {e}")
        log_and_store(f"RAG: Error to save on Redis: {e}", config)
        raise

def base_rag_redis_pipeline_controller(    
    prompt: str,
    query: str,
    config: AppConfig,
    redis_client: Redis,
    redis_url: str,
    k: int = 6,
    chunk_size: int = 8000,
) -> str:
    """Executar RAG com uma lista de arquivos"""
    redis_key_status = f"status:{config.user}:{config.task_id}:{config.type_of_analysis}"
    sufix = f"{config.user}:{config.task_id}:{config.type_of_analysis}"
    file_list_sufix = f"file:{sufix}*"

    try:
        file_keys_list = redis_client.keys(file_list_sufix)
        file_name_list = []

        for redis_key_file in file_keys_list:
            # Creating embeddings
            log_and_store(f"Creating Embedding: {redis_key_file}", config)
            
            content = redis_client.hget(redis_key_file, 'file').decode('utf-8')
            file_name = redis_client.hget(redis_key_file, 'file_name').decode('utf-8')
            embedding = Embeddings()
            embedding.azure_create_embedding(content=content, file_name=file_name, chunk_size=chunk_size)

            # Armazenar o conteúdo tokenizado no Redis
            tokenized_content = str(embedding.text_splitted_list)
            redis_client.hset(redis_key_file, mapping={'tokenized': tokenized_content})

            # Carregar embeddings no armazenamento de vetores Redis
            embedding.prepare_data()
            vector_store = RedisVectorStore(redis_url=redis_url)
            vector_store.load_data(embedding, config)
            
            log_and_store(f"Embeddings loaded", config)
            file_name_list.append(file_name)

        # RAG
        rag_obj = RAGRedis(config=config, redis_url=redis_url, k=k)
        rag_obj.rag(query, prompt)

        # Prepara os dados para salvar no redis
        data_to_save = SaveRedisPydantic(
            response = json.dumps(rag_obj.response),
            context =  json.dumps(rag_obj.context),
            usage =  json.dumps(rag_obj.usage),
            response_json =  json.dumps(rag_obj.response_json),
            messages =  json.dumps(rag_obj.messages),
            type_of_analysis =  json.dumps(config.type_of_analysis),
            technique = json.dumps("RAG"),
            evaluation = 0,
            observation = "",
            file_names = json.dumps(file_name_list)
        )

        redis_key = ct_response.save_response_to_redis(config, data_to_save )
        return redis_key

    except Exception as e:
        raise