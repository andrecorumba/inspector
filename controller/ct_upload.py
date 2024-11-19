from typing import Any

from controller.ct_log import log_and_store
from model.tika import TikaParser
from model.config_schema import (
    AppConfig, 
    REDIS_CLIENT,
    TIKA_SERVER_ENDPOINT
    )


def upload_controller(file_bytes: bytes, file_name: str, config: AppConfig) -> Any:
    """
    Handles the processing of an uploaded file, including content extraction, embedding creation, 
    and storage in Redis.

    Args:
        file_bytes (bytes): The binary content of the uploaded file.
        file_name (str): The name of the uploaded file.
        config (AppConfig): The configuration object containing user, task, and analysis details.

    Returns:
        Any: The Redis key for the saved file data, or None if an error occurs during processing.
    """

    sufix = f"{config.user}:{config.task_id}:{config.type_of_analysis}"

    try:
        # Analyze the file content using Tika
        tika_parser = TikaParser(tika_server=TIKA_SERVER_ENDPOINT)
        content = tika_parser.tika_parser_from_bytes(file_bytes)
        file_hash = tika_parser.hash_file_bytes(file_bytes)
        
        # Take only the first 16 characters of the hash
        redis_key_file = f"file:{sufix}:{file_hash[:16]}"
        
        log_and_store(f"Tika: Extracted file {file_name}", config)

        if content is None:
            log_and_store(f"Tika: Error extracting file {file_name}", config)
            return

        # Store the parsed content in Redis
        REDIS_CLIENT.hset(redis_key_file, mapping={
            'file_name': file_name,
            'file': content,
            'tokenized': '',
            })
        log_and_store(f"Tika: File saved: {redis_key_file}", config)
        
        return redis_key_file

    except Exception as e:
        log_and_store(f"Tika: Error in upload_controller: {e}", config)
        raise