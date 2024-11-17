from call_endpoints import upload_endpoint
from typing import Any, Dict

def upload_file(uploaded_file: Any, id: str, type_of_analysis: str, user: str) -> Dict:
    """
    Uploads the file for analysis.

    Args:
        uploaded_file (Any): The file object to be uploaded.
        id (str): Unique identifier for the task.
        type_of_analysis (str): The type of analysis to be performed.
        user (str): The username or identifier of the user.

    Returns:
        dict: The response from the API after the upload request.
    """
    headers = {
        'accept': 'application/json',
    }
    files = {
        'file': (
            uploaded_file.name,
            uploaded_file,
            uploaded_file.type,
        ),
    }
    params = {
        'task_id': id,
        'type_of_analysis': type_of_analysis,
        'user': user
    }

    try:
        response_request = upload_endpoint(headers, files, params)
        return response_request
    except Exception as e:
        return {"error": f"File upload failed: {e}"}