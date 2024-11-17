from pydantic import BaseModel, ValidationError

import aiohttp

from model.config_schema import (
    AppConfig, 
    REDIS_CLIENT, 
    REDIS_URL,
    TrilhasPessoalItems,
    )

from controller import ct_rag, ct_prompts
from controller.ct_log import log_and_store
from controller.ct_ecgu import request_attachments, load_files_with_tika

import aiohttp
from aiohttp import ClientResponseError
from fastapi import HTTPException

async def a_search_ecgu_trilhas(config: AppConfig):
    """Método assíncrono para carregar o JSON da tarefa de monitoramento de trilhas do e-CGU."""
    url = f'https://eaud.cgu.gov.br/api/auth/tarefa/{config.task_id}/dto/json'
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'chave-api': config.ecgu_api_key,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                try:
                    response.raise_for_status()
                except ClientResponseError as cre:
                    if cre.status == 403:
                        # Lida especificamente com o erro 403
                        log_and_store(f"Erro Acesso negado ao baixar a tarefa: {cre}", config)
                        # Levanta uma exceção HTTP com status 403
                        raise HTTPException(status_code=403, detail="Acesso negado à tarefa. Verifique suas credenciais e permissões.")
                    else:
                        # Lida com outros erros HTTP
                        log_and_store(f"Erro HTTP no e-CGU ao baixar a tarefa: {cre}", config)
                        raise HTTPException(status_code=cre.status, detail=f"Erro no e-CGU ao acessar a tarefa: {cre}")
                # Processa a resposta JSON
                trilhas_pessoal_dict = await response.json()
                if trilhas_pessoal_dict.get('assunto') and trilhas_pessoal_dict['atividade'] == "Trilhas de Pessoal":
                    try:
                        content_task = TrilhasPessoalItems(
                            id_tarefa_trilhas_pessoal=config.task_id,
                            titulo=trilhas_pessoal_dict.get('titulo'),
                            descricao_complementar=trilhas_pessoal_dict.get('campos', {}).get('descrCompl', {}).get('valor'),
                            justificativa_gestor=trilhas_pessoal_dict.get('campos', {}).get('justificativa', {}).get('valor'),
                            parecer_gestor=trilhas_pessoal_dict.get('campos', {}).get('parecerGestorAudContinua', {}).get('valor', {}),
                            data_ultima_modificacao=trilhas_pessoal_dict.get('dataUltimaModificacao')
                        )
                        log_and_store("Tarefa baixada do e-aud", config)
                        return content_task
                    except ValidationError as ve:
                        log_and_store(f"Erro de validação dos dados: {ve}", config)
                        raise HTTPException(status_code=422, detail=f"Erro de validação: {ve}")
                else:
                    # Caso a resposta não seja a esperada
                    log_and_store("Erro Tarefa não encontrada ou atividade incorreta.", config)
                    raise HTTPException(status_code=404, detail="Tarefa não encontrada ou atividade incorreta.")
    except aiohttp.ClientError as e:
        log_and_store(f"Erro no e-CGU ao baixar a tarefa: {e}", config)
        raise HTTPException(status_code=500, detail=f"Erro de conexão: {e}")


def module_trilhas_pessoal_ecgu(config: AppConfig, content_task: TrilhasPessoalItems):
    # content_task = await a_search_ecgu_trilhas(config)
    attachment = request_attachments(config)
    file_list_keys = load_files_with_tika(config, attachment)

    query = content_task.titulo
    items_str = content_task.model_dump_json()

    redis_key_response = ct_rag.base_rag_redis_pipeline_controller(
        prompt=ct_prompts.PROMPT_TRILHAS_PESSOAL.format(items=items_str),
        query=query,
        config=config,
        redis_client=REDIS_CLIENT,
        k=6,
        redis_url=REDIS_URL,
        chunk_size=2000,
        )
    return redis_key_response


