from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from model.config_schema import AppConfig
from modules import medical
import logging

router_medical = APIRouter()

logger = logging.getLogger(__name__)

@router_medical.post("/medical")
async def run(config: AppConfig, background_tasks: BackgroundTasks):
    """
    Initiates a medical analysis task asynchronously.

    This function queues a medical analysis task using the provided configuration. 
    The task is executed in the background, and the response includes the task ID.

    Args:
        config (AppConfig): Configuration object containing details such as task ID, user, 
            and analysis type.
        background_tasks (BackgroundTasks): FastAPI's background task manager to handle
            asynchronous task execution.

    Returns:
        JSONResponse: A JSON response containing the task ID, e.g., {"task_id": <task_id>}.

    Raises:
        HTTPException: If an error occurs while queuing the task, an HTTP 500 error is returned 
        with a relevant message.
    """
    try:
        background_tasks.add_task(medical.module_medical, config)
        logger.info(f"Task {config.task_id} has been queued successfully.")
        return JSONResponse({'task_id': config.task_id})
    except Exception as e:
        logger.error(f"Failed to queue task {config.task_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while queuing the task.")