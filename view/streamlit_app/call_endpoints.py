import requests
import logging
import os
# from dotenv import load_dotenv, find_dotenv

# # Load environment variables
# load_dotenv(find_dotenv())
# API_HOST = os.getenv("API_HOST", "localhost")
# API_PORT = os.getenv("API_PORT", "8000") 

API_HOST = "fastapi"
API_PORT = "8000"

logger = logging.getLogger(__name__)

def call_endpoint(api_route: str, parameters: dict) -> dict:
    """
    Makes a POST request to a specified API endpoint.

    This function sends a POST request to the given RAG endpoint with the provided parameters
    and returns the JSON response.

    Args:
        api_route (str): The API route to which the POST request is sent.
        parameters (dict): The parameters to be included in the POST request body.

    Returns:
        dict: The JSON response from the API.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the HTTP request,
        the exception is logged and re-raised.
    """
    url = f'http://{API_HOST}:{API_PORT}{api_route}'
    logger.info(f'Sending POST request to {url}')
    try:
        response = requests.post(url, json=parameters)
        response.raise_for_status()
        response_json = response.json()
        logger.debug(f'Received response: {response_json}')
        return response_json
    except requests.exceptions.RequestException as e:
        logger.error(f'Request error to {url}: {e}')
        raise


def upload_endpoint(headers: dict, files: dict, params: dict) -> dict:
    """
    Makes a POST request to upload PDF files to a specified API endpoint.

    This function sends a file upload request to the `/upload` endpoint with the provided headers,
    files, and parameters. It returns the JSON response from the API.

    Args:
        headers (dict): Headers to include in the POST request, such as authentication tokens.
        files (dict): Files to upload, with keys representing the field names and values as file objects.
        params (dict): Additional parameters to include in the request query string.

    Returns:
        dict: The JSON response from the API.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the HTTP request,
        the exception is logged and re-raised.
    """
    url = f'http://{API_HOST}:{API_PORT}/upload'
    logger.info(f'Sending POST request to {url}')
    try:
        response = requests.post(url, headers=headers, files=files, params=params)
        response.raise_for_status()
        response_json = response.json()
        logger.debug(f'Received response: {response_json}')
        return response_json
    except requests.exceptions.RequestException as e:
        logger.error(f'Request error to {url}: {e}')
        raise