
import requests

from model.config_schema import (
    AppConfig, 
    RecomendationItems,
    REDIS_CLIENT, 
    REDIS_URL,
    )

from controller import ct_rag, ct_prompts
from controller.ct_log import log_and_store
import logging
from model.tika import TikaParser
from controller import ct_upload

# Função para baixar os anexos
def request_attachments(config: AppConfig):
    """Método Síncrono para request do json de anexos da tarefa do e-CGU.
    Serve tanto para a tarefa de Monitoramento de Recomendações quanto para outras tarefas.
    url exemplo: https://eaud.cgu.gov.br/api/auth/tarefa/1375160/arquivos"""
    url = f'https://eaud.cgu.gov.br/api/auth/tarefa/{config.task_id}/arquivos'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'chave-api': config.ecgu_api_key,
    }
    try:
        response_eaud_request = requests.request('GET', url, headers=headers)
        response_eaud_request.raise_for_status()
        attachment = response_eaud_request.json()

        # Validação simples no json
        if 'recordsTotal' in attachment:
            log_and_store(f"{config.type_of_analysis}: tarefa baixada do e-aud", config)
            return attachment
        else:
            return {}
    except requests.exceptions.RequestException as e:
        log_and_store(f"{config.type_of_analysis}:Erro ao baixar tarefa do e-CGU: {e}", config)
        raise


def load_files_with_tika(config: AppConfig, attachment: dict):
    """Método para carregar documentos langchain dos anexos de recomendações do EAUD com Apache Tika."""
    file_list_keys = []
    if attachment == {}:
        return
    for attachment in attachment['data']:
        url = f"https://eaud.cgu.gov.br/api/auth/tarefa/{attachment['idTarefa']}/arquivo/{attachment['idArquivo']}"
        headers = {
            'Content-Type': 'application/pdf;charset=UTF-8',
            'chave-api': config.ecgu_api_key,
            }
        try: 
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                uploaded = ct_upload.upload_controller(
                                        file_bytes=response.content,
                                        file_name=attachment['nomeArquivo'],
                                        config=config,
                                    )
                file_list_keys.append(uploaded)
                log_and_store(f"{config.type_of_analysis}: Arquivos Baixados e carregados", config)
        except Exception as e:
            log_and_store(f"{config.type_of_analysis}:Erro ao fazer download dos arquivos do e-CGU {e}", config)
            raise
    return file_list_keys

