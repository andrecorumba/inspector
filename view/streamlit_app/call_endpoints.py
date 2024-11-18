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
    """Makes a POST request to a specific RAG endpoint."""
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
    """Makes a POST request to upload PDF files to a specific endpoint."""
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