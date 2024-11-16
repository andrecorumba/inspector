import os
from redis import Redis
from pydantic import BaseModel, Field
from typing import Optional
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_CLIENT = Redis(host=REDIS_HOST,port=REDIS_PORT)
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"
TIKA_SERVER_ENDPOINT = os.getenv("TIKA_SERVER_ENDPOINT")

API_HOST = os.getenv("API_HOST")
API_PORT = os.getenv("API_PORT")

class AppConfig(BaseModel):
    user: str
    task_id: str
    type_of_analysis: str
    ecgu_api_key: Optional[str] = None

class RecomendationItems(BaseModel):
    id_tarefa_monitoramento: str
    texto_recomendacao: str
    texto_manifestacao_unidade_auditada: str
    texto_posicionamento_anterior: str
    has_attachments: bool

class SaveRedisPydantic(BaseModel):
    response: str
    context: Optional[str] = Field(default="")
    usage: str
    response_json: str
    messages: str
    type_of_analysis: str
    technique: Optional[str] = Field(default="")
    evaluation: Optional[int] = 0
    observation: Optional[str] = Field(default="")
    file_names: Optional[str] = Field(default="")

class TrilhasPessoalItems(BaseModel):
    id_tarefa_trilhas_pessoal: int
    titulo: Optional[str]
    descricao_complementar: Optional[str]
    justificativa_gestor: Optional[str]
    # parecer_gestor: Optional[str]
    parecer_gestor: Optional[dict]
    data_ultima_modificacao: Optional[str]

class Evaluation(BaseModel):
    evaluation: int
    observation: Optional[str] = None