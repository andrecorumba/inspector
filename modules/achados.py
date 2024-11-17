from model.config_schema import (
    AppConfig,
    REDIS_CLIENT,
    SaveRedisPydantic,
    )

from model.chats import AzureChatInsight
from controller.ct_prompts import PROMPT_ACHADOS
from controller import ct_response, ct_log

from model.split_text import SplitText


import json

def module_achados(config: AppConfig):
    file_list_sufix = f"file:{config.user}:{config.task_id}:{config.type_of_analysis}*"
    file_keys_list = REDIS_CLIENT.keys(file_list_sufix)
    if file_keys_list == []:
        ct_log.log_and_store("Não encontrada chave com Matriz de Achados", config)
        return
    
    redis_key_file = file_keys_list[0]
    content = REDIS_CLIENT.hget(redis_key_file, 'file').decode('utf-8')

    # Limpar arquivo
    cleaned_text = SplitText()._clean_text(content=content)

    completion = AzureChatInsight()
    completion.invoke(
        prompt=PROMPT_ACHADOS,
        context=" ".join(cleaned_text),
        persona="Você é um assistente que revisa relatórios de auditoria governamental.",
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

    redis_key = ct_response.save_response_to_redis(config, data_to_save)
    return redis_key



