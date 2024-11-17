import requests

from model.config_schema import (
    AppConfig, 
    RecomendationItems,
    SaveRedisPydantic,
    REDIS_CLIENT, 
    REDIS_URL,
    )

from controller import ct_rag, ct_prompts, ct_response
from controller.ct_log import log_and_store
import logging
from model.tika import TikaParser
from model.chats import AzureChatInsight
from controller import ct_upload
from controller.ct_ecgu import request_attachments, load_files_with_tika

import json


def module_recomendacao(
        config: AppConfig, 
        items: RecomendationItems
        ):
    query = items.texto_recomendacao

    items_str = f"""
        Recomendação da Auditoria: {items.texto_recomendacao},
        Manifestação da Unidade Auditada: {items.texto_manifestacao_unidade_auditada},
        Posicionamento Anterior da Auditoria: {items.texto_posicionamento_anterior},
    """
    
    if items.has_attachments:
        redis_key_response = ct_rag.base_rag_redis_pipeline_controller(
            prompt=ct_prompts.PROMPT_RECOMENDACAO.format(items=items_str),
            query=query,
            config=config,
            redis_client=REDIS_CLIENT,
            k=6,
            redis_url=REDIS_URL,
            chunk_size=2000,
            )
        
        return redis_key_response

    else:
        completion = AzureChatInsight()
        completion.invoke(
            prompt=ct_prompts.PROMPT_RECOMENDACAO.format(items=items_str),
            context=" ",
            persona="Você é um auditor interno governamental especializado em análise do atendimento de recomendações de auditoria."
            )
        
        # Prepara os dados para salvar no redis
        data_to_save = SaveRedisPydantic(
            response = json.dumps(completion.response),
            context =  json.dumps({"context": completion.context}),
            usage =  json.dumps(completion.usage),
            response_json =  json.dumps(completion.response_json),
            messages =  json.dumps(completion.messages),
            type_of_analysis =  json.dumps(config.type_of_analysis),
        )

        redis_key_response = ct_response.save_response_to_redis(config, data_to_save)
        return redis_key_response

async def a_search_eaud_recomendation(config: AppConfig):
    """Método assíncrono para carregar o json da tarefa de monitoramento de recomendações do EAUD."""
    url = f'https://eaud.cgu.gov.br/api/auth/tarefa/{config.task_id}/dto/json'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'chave-api': config.ecgu_api_key,
    }
    try:
        response_eaud_request = requests.request('GET', url, headers=headers)
        response_eaud_request.raise_for_status()
        monitoring_dict = response_eaud_request.json()
        if 'assunto' in monitoring_dict:
            content_task = {}
            content_task['id_tarefa_monitoramento'] = config.task_id
            content_task['texto_recomendacao'] = monitoring_dict['campos']['detalhesMonitoramento']['valor']
            content_task['texto_manifestacao_unidade_auditada'] = monitoring_dict['campos']['textoUltimaManifestacao']['valor']
            content_task['texto_posicionamento_anterior'] = monitoring_dict['campos']['textoUltimoPosicionamento']['valor']
            log_and_store("Recomendação: tarefa baixada do e-aud", config)
            return content_task
    except requests.exceptions.RequestException as e:
        log_and_store(f"Erro ao baixar a tarefa {e}", config)
        raise

def module_recomendation_ecgu(config: AppConfig, items: RecomendationItems):
    attachment = request_attachments(config)
    file_list_keys = load_files_with_tika(config, attachment)

    query = items.texto_recomendacao
    items_str = f"""
        Recomendação da Auditoria: {items.texto_recomendacao},
        Manifestação da Unidade Auditada: {items.texto_manifestacao_unidade_auditada},
        Posicionamento Anterior da Auditoria: {items.texto_posicionamento_anterior},
        """
    redis_key_response = ct_rag.base_rag_redis_pipeline_controller(
        prompt=ct_prompts.PROMPT_RECOMENDACAO.format(items=items_str),
        query=query,
        config=config,
        redis_client=REDIS_CLIENT,
        k=6,
        redis_url=REDIS_URL,
        chunk_size=2000,
        )
    return redis_key_response




# # Função para baixar os anexos
# def request_attachments(config: AppConfig):
#     """Método Síncrono para request do json de anexos da tarefa do e-CGU.
#     Serve tanto para a tarefa de Monitoramento de Recomendações quanto para outras tarefas.
#     url exemplo: https://eaud.cgu.gov.br/api/auth/tarefa/1375160/arquivos"""
#     url = f'https://eaud.cgu.gov.br/api/auth/tarefa/{config.task_id}/arquivos'
#     headers = {
#         'Content-Type': 'application/json;charset=UTF-8',
#         'chave-api': config.ecgu_api_key,
#     }
#     try:
#         response_eaud_request = requests.request('GET', url, headers=headers)
#         response_eaud_request.raise_for_status()
#         attachment = response_eaud_request.json()

#         # Validação simples no json
#         if 'recordsTotal' in attachment:
#             log_and_store(f"{config.type_of_analysis}: tarefa baixada do e-aud", config)
#             return attachment
#         else:
#             return {}
#     except requests.exceptions.RequestException as e:
#         log_and_store(f"{config.type_of_analysis}:Erro ao baixar tarefa do e-CGU: {e}", config)
#         raise


# def load_files_with_tika(config: AppConfig, attachment: dict):
#     """Método para carregar documentos langchain dos anexos de recomendações do EAUD com Apache Tika."""
#     file_list_keys = []
#     if attachment == {}:
#         return
#     for attachment in attachment['data']:
#         url = f"https://eaud.cgu.gov.br/api/auth/tarefa/{attachment['idTarefa']}/arquivo/{attachment['idArquivo']}"
#         headers = {
#             'Content-Type': 'application/pdf;charset=UTF-8',
#             'chave-api': config.ecgu_api_key,
#             }
#         try: 
#             response = requests.get(url, headers=headers)
#             if response.status_code == 200:
#                 uploaded = ct_upload.upload_controller(
#                                         file_bytes=response.content,
#                                         file_name=attachment['nomeArquivo'],
#                                         config=config,
#                                     )
#                 file_list_keys.append(uploaded)
#                 log_and_store(f"{config.type_of_analysis}: Arquivos Baixados e carregados", config)
#         except Exception as e:
#             log_and_store(f"{config.type_of_analysis}:Erro ao fazer download dos arquivos do e-CGU {e}", config)
#             raise
#     return file_list_keys

