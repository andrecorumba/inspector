from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Response
from fastapi.responses import JSONResponse

from redis import Redis
from pydantic import BaseModel
import os

from model.config_schema import AppConfig
from controller import ct_rag, ct_upload, ct_response

from view.api.route_medical import router_medical
from view.api.route_responses import router_response

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from model.config_schema import (
    AppConfig, 
    REDIS_CLIENT,
    REDIS_URL,
    TIKA_SERVER_ENDPOINT
    )


api = FastAPI()

@api.get("/")
def read_root():
    return {"Hello": "World"}

api.include_router(router_response)

@api.get("/status/{user}")
async def status_user(user: str):
    status = ct_response.status_by_user(user=user)
    return status

@api.post("/upload")
async def upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...), 
    task_id: str = '1234', 
    type_of_analysis: str = 'anexo', 
    user: str = 'convidado',
    )->dict:
    """Endpoint to upload files. 
    type_of_document: 'documento_entendimento' | 'matriz_riscos_controle' | 'matriz_planejamento' """
    
    file_bytes = await file.read()
    file_name = file.filename.split("/")[-1]

    config = AppConfig(
        user=user, 
        task_id=task_id,
        type_of_analysis=type_of_analysis,
        )

    uploaded = ct_upload.upload_controller(
        file_bytes=file_bytes,
        file_name=file_name,
        config=config,
    )

    return {"key_file": uploaded}


class RagItems(BaseModel):
    prompt: str
    query: str

@api.post("/rag")
async def rag(background_tasks: BackgroundTasks, config: AppConfig, items: RagItems):
   redis_key_response = background_tasks.add_task(ct_rag.base_rag_redis_pipeline_controller,
        prompt=items.prompt,
        query=items.query,
        config=config,
        redis_client=REDIS_CLIENT,
        k=6,
        redis_url=REDIS_URL,
        chunk_size=8000,
        )
   return JSONResponse({"redis_key_response": redis_key_response})

api.include_router(router_medical)