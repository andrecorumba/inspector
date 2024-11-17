from model.config_schema import (
    AppConfig, 
    REDIS_CLIENT, 
    REDIS_URL,
    )
from controller import ct_rag, ct_prompts

def module_documento_entendimento(config: AppConfig):
    query = """O documento possui objetivos, estratégias, prioridades, 
        ambiente de controle, estrutura de governança, direcionadores de 
        unidade auditada, informações relevantes sobre objeto de auditoria, 
        objetivos, responsabilidades, recursos, fluxograma, pontos críticos 
        de controle, histórico de auditorias, identificação e avaliação de 
        riscos e controles, elaboração da matriz de planejamento."""
    
    redis_key_response = ct_rag.base_rag_redis_pipeline_controller(
        prompt=ct_prompts.PROMPT_SUPERVISAO_DOCUMENTO_ENTENDIMENTO,
        query=query,
        config=config,
        redis_client=REDIS_CLIENT,
        k=6,
        redis_url=REDIS_URL,
        chunk_size=8000,
        )
    
    return redis_key_response

def module_matriz_riscos_controle(config: AppConfig):
    query = """O documento possui os objetivos de auditoria, 
        identificação de riscos, causas e consequências dos riscos,
        avaliação de risco (impacto e probabilidade), controles internos,
        risco de controle, avaliação preliminar dos auditores, questões de auditoria
        testes substantivos e Testes de controle?"""
    
    redis_key_response = ct_rag.base_rag_redis_pipeline_controller(
        prompt=ct_prompts.PROMPT_SUPERVISAO_MATRIZ_DE_RISCOS_CONTROLE,
        query=query,
        config=config,
        redis_client=REDIS_CLIENT,
        k=6,
        redis_url=REDIS_URL,
        chunk_size=8000,
        )
    
    return redis_key_response

def module_matriz_planejamento(config: AppConfig):
    query = """O documento possui as questões de auditoria, as subquestões de auditoria,
        os testes, os critérios e demais informações de planejamento?"""
    
    redis_key_response = ct_rag.base_rag_redis_pipeline_controller(
        prompt=ct_prompts.PROMPT_SUPERVISAO_MATRIZ_PLANEJAMENTO,
        query=query,
        config=config,
        redis_client=REDIS_CLIENT,
        k=6,
        redis_url=REDIS_URL,
        chunk_size=8000,
        )
    
    return redis_key_response

def module_plano_amostral(config: AppConfig):
    query = """Os planos amostrais documentam de forma apropriada a população objeto da análise,
        os itens selecionados na amostra, a representatividade da amostra em relação à população e  
        os critérios de seleção utilizados?"""
    
    redis_key_response = ct_rag.base_rag_redis_pipeline_controller(
        prompt=ct_prompts.PROMPT_SUPERVISAO_PLANO_AMOSTRAL,
        query=query,
        config=config,
        redis_client=REDIS_CLIENT,
        k=6,
        redis_url=REDIS_URL,
        chunk_size=8000,
        )
    
    return redis_key_response