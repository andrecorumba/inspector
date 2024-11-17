import requests
import logging
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = os.getenv("API_PORT", "8000")

logger = logging.getLogger(__name__)

def call_endpoint(api_route: str, parameters: dict) -> dict:
    """
    Makes a POST request to a specific RAG endpoint.

    Args:
        api_route (str): The API route to call.
        parameters (dict): The parameters to send in the POST request.

    Returns:
        dict: The response from the API in JSON format or an error message.
    """
    url = f'http://{API_HOST}:{API_PORT}{api_route}'
    logger.info(f'Sending POST request to {url}')
    try:
        response = requests.post(url, json=parameters)
        response.raise_for_status()
        response_json = response.json()
        logger.debug(f'Received response: {response_json}')
        return response_json
    except requests.exceptions.HTTPError as http_err:
        logger.error(f'HTTP error during request to {url}: {http_err}')
        try:
            error_content = response.json()
            error_message = error_content.get('detail', str(http_err))
        except ValueError:
            error_message = str(http_err)
        return {'error': error_message}
    except requests.exceptions.RequestException as e:
        logger.error(f'Request error to {url}: {e}')
        return {'error': f"Connection error: {e}"}


def upload_endpoint(headers: dict, files: dict, params: dict) -> dict:
    """
    Makes a POST request to upload PDF files to a specific endpoint.

    Args:
        headers (dict): The headers for the request.
        files (dict): The files to upload in the request.
        params (dict): The additional parameters for the request.

    Returns:
        dict: The response from the API in JSON format or an error message.
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