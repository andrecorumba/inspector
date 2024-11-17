from fastapi.responses import JSONResponse
from fastapi import APIRouter, Path, HTTPException

from controller import ct_response
from model.config_schema import Evaluation

router_response = APIRouter()

@router_response.get("/response/{rag_redis_key}")
async def get_response(rag_redis_key: str = Path(..., description="Redis Key. e.g.: rag:user:8719:medical")):
    """
    Fetches the response associated with a Redis key.

    Args:
        rag_redis_key (str): Redis key for the analysis.

    Returns:
        JSONResponse: The analysis response content.
    """
    try:
        response = ct_response.response_controller(rag_redis_key)
        if not response:
            raise HTTPException(status_code=404, detail="Response not found")
        return JSONResponse(content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router_response.get("/response/per-user/{user}")
async def get_responses_by_user(user: str = Path(..., description="User e.g.: user")):
    """
    Fetches all responses associated with a user.

    Args:
        user (str): User identifier.

    Returns:
        dict: A dictionary of responses for the user.
    """
    try:
        response = ct_response.responses_by_user(user=user)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router_response.get("/response/use/{rag_redis_key}")
async def get_usage(rag_redis_key: str = Path(..., description="Redis Key. e.g.: rag:user:8719:medical")):
    """
    Fetches the token usage associated with a Redis key.

    Args:
        rag_redis_key (str): Redis key for the analysis.

    Returns:
        JSONResponse: Token usage details.
    """
    try:
        usage = ct_response.usage_controller(rag_redis_key)
        return JSONResponse(content=usage)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router_response.get("/response/context/{rag_redis_key}")
async def get_context(rag_redis_key: str = Path(..., description="Redis Key. e.g.: rag:user:8719:medical")):
    """
    Fetches the context information associated with a Redis key.

    Args:
        rag_redis_key (str): Redis key for the analysis.

    Returns:
        JSONResponse: Context details.
    """
    try:
        context = ct_response.context_controller(rag_redis_key)
        return JSONResponse(content=context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router_response.get("/response/files/{rag_redis_key}")
async def get_files(rag_redis_key: str = Path(..., description="Redis Key. e.g.: rag:user:8719:medical")):
    """
    Fetches the file names associated with a Redis key.

    Args:
        rag_redis_key (str): Redis key for the analysis.

    Returns:
        JSONResponse: File names.
    """
    try:
        files = ct_response.file_names_controller(rag_redis_key)
        return JSONResponse(content=files)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router_response.get("/response/detail/{rag_redis_key}")
async def get_detail(rag_redis_key: str = Path(..., description="Redis Key. e.g.: rag:user:8719:medical")):
    """
    Fetches the detailed response information associated with a Redis key.

    Args:
        rag_redis_key (str): Redis key for the analysis.

    Returns:
        JSONResponse: Detailed response information.
    """
    try:
        detail = ct_response.detail_controller(rag_redis_key)
        return JSONResponse(content=detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router_response.get("/response/messages/{rag_redis_key}")
async def get_messages(rag_redis_key: str = Path(..., description="Redis Key. e.g.: rag:user:8719:medical")):
    """
    Fetches the messages associated with a Redis key.

    Args:
        rag_redis_key (str): Redis key for the analysis.

    Returns:
        JSONResponse: Message details.
    """
    try:
        messages = ct_response.message_controller(rag_redis_key)
        return JSONResponse(content=messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router_response.post("/response/evaluation/{rag_redis_key}")
async def post_evaluation(rag_redis_key: str, evaluation_items: Evaluation):
    """
    Submits an evaluation for a response.

    Args:
        rag_redis_key (str): Redis key for the analysis.
        evaluation_items (Evaluation): Evaluation data.

    Returns:
        JSONResponse: The evaluation result.
    """
    try:
        evaluation = ct_response.evaluation_response(rag_redis_key, evaluation_items)
        return JSONResponse(content=evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")


@router_response.get("/response/evaluation/{rag_redis_key}")
async def get_evaluation(rag_redis_key: str = Path(..., description="Redis Key. e.g.: rag:user:8719:medical")):
    """
    Fetches the evaluation associated with a Redis key.

    Args:
        rag_redis_key (str): Redis key for the analysis.

    Returns:
        JSONResponse: Evaluation details.
    """
    try:
        evaluation = ct_response.evaluation_controller(rag_redis_key)
        return JSONResponse(content=evaluation)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")