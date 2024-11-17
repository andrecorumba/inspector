from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from model.config_schema import AppConfig
from modules import etp
import logging

router_medical = APIRouter()

logger = logging.getLogger(__name__)

@router_medical.post("/medical")
async def run(config: AppConfig, background_tasks: BackgroundTasks):
    """
    Endpoint to initiate a medical analysis task.

    Args:
        config (AppConfig): Configuration for the analysis task.
        background_tasks (BackgroundTasks): FastAPI BackgroundTasks for asynchronous task execution.

    Returns:
        JSONResponse: A JSON response with the task ID.
    """
    try:
        background_tasks.add_task(etp.module_etp_tic, config)
        logger.info(f"Task {config.task_id} has been queued successfully.")
        return JSONResponse({'task_id': config.task_id})
    except Exception as e:
        logger.error(f"Failed to queue task {config.task_id}: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while queuing the task.")