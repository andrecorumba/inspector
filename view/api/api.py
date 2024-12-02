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
    )


api = FastAPI()

@api.get("/")
def read_root():
    """
    Root endpoint for the API.

    This endpoint serves as a simple health check or welcome message for the API.

    Returns:
        dict: A dictionary containing a greeting message, e.g., {"Hello": "World"}.
    """
    return {"Hello": "World"}

api.include_router(router_response)

@api.get("/status/{user}")
async def status_user(user: str):
    """
    Retrieves the status of tasks for a given user.

    This endpoint fetches the current status of all tasks associated with a specific user.

    Args:
        user (str): The identifier of the user whose task status is being queried.

    Returns:
        dict: A dictionary containing the status of tasks for the user.
    """
    status = ct_response.status_by_user(user=user)
    return status

@api.post("/upload")
async def upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...), 
    task_id: str = '1234', 
    type_of_analysis: str = 'medical', 
    user: str = 'user',
    )->dict:
    """
        Handles file upload and processing via a POST endpoint.

        This endpoint allows users to upload a file for analysis. The type of analysis can
        be specified as 'medical', 'document', or 'other'. The uploaded file is processed 
        asynchronously in the background.

        Args:
            background_tasks (BackgroundTasks): FastAPI's background task manager to handle
                post-upload processing.
            file (UploadFile): The file to be uploaded. Must be provided in the request.
            task_id (str, optional): An identifier for the task. Defaults to '1234'.
            type_of_analysis (str, optional): Specifies the type of analysis for the uploaded file.
                Can be 'medical', 'document', or 'other'. Defaults to 'medical'.
            user (str, optional): The user initiating the upload. Defaults to 'user'.

        Returns:
            dict: A dictionary containing the key for the uploaded file, e.g., {"key_file": uploaded}.
    """
    
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
   """
    Executes a RAG (Retrieval-Augmented Generation) pipeline task asynchronously.

    This function triggers a background task to run the RAG pipeline using the provided
    configuration, query, and prompt details. The results are stored in Redis.

    Args:
        background_tasks (BackgroundTasks): FastAPI's background task manager to handle
            the asynchronous execution of the RAG pipeline.
        config (AppConfig): Configuration object containing user, task, and analysis details.
        items (RagItems): Object containing the prompt and query for the RAG pipeline.

    Returns:
        JSONResponse: A JSON response containing the Redis key associated with the RAG task results,
        e.g., {"redis_key_response": <redis_key>}.
    """
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