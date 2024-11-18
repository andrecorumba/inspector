from model.config_schema import (
    AppConfig, 
    REDIS_CLIENT, 
    REDIS_URL,
    )
from controller import ct_rag, ct_prompts, ct_response

def module_etp_tic(config: AppConfig) -> str:
    """
    Extracts specific medical parameters from a data source using a Redis-based RAG pipeline.

    Args:
        config (AppConfig): Configuration object containing user, task, and analysis information.

    Returns:
        str: The Redis key associated with the result of the RAG pipeline execution.
    """

    query = """Extract the parâmeters: Creatinine, Hemoglobin, White Blood Cell Count (WBC),Red Blood Cell Count (RBC)
	Platelet Count, Hematocrit, Glucose, Cholesterol (Total), LDL Cholesterol, HDL Cholesterol, Triglycerides, 
    Urea, Blood Urea Nitrogen (BUN), Liver Function Tests (ALT, AST), Bilirubin (Total and Direct), Albumin, 
    Calcium (Serum), Sodium (Serum), Potassium (Serum), Thyroid Stimulating Hormone (TSH)"""
    
    rag_redis_key = ct_rag.base_rag_redis_pipeline_controller(
        prompt=ct_prompts.PROMPT_MEDIAL,
        query=query,
        config=config,
        redis_client=REDIS_CLIENT,
        k=6,
        redis_url=REDIS_URL,
        chunk_size=4000,
        )
    
    return rag_redis_key