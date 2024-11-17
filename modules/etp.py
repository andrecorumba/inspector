from model.config_schema import (
    AppConfig, 
    REDIS_CLIENT, 
    REDIS_URL,
    )
from controller import ct_rag, ct_prompts, ct_response

def module_etp_tic(config: AppConfig):
    query = """O documento traz a Definição das necessidades de negócio e tecnológicas, 
    a Solução tecnológica escolhida resolve o problema do órgão ou atende à necessidade descrita, 
    o Quantitativo de bens e serviços necessários, 
    a Análise comparativa de soluções, 
    a Análise comparativa de custos (TCO), 
    a Fundamentação da forma de pagamento,
    o Ganho de eficiência na adesão a ata de registro de preços (se aplicável)."""
    
    rag_redis_key = ct_rag.base_rag_redis_pipeline_controller(
        prompt=ct_prompts.PROMPT_ETP_TIC,
        query=query,
        config=config,
        redis_client=REDIS_CLIENT,
        k=6,
        redis_url=REDIS_URL,
        chunk_size=4000,
        )
    
    return rag_redis_key