# Inspector

Inspector is a Proof of Concept (POC) for a Python-based web application designed to analyze documents using cutting-edge AI technologies.

## Key Features

### Insight Extraction

- Large Language Models (LLMs): Utilizes advanced LLMs for user-driven document analysis, seamlessly integrated with Azure OpenAI services.
- Retrieval-Augmented Generation (RAG): Enhances information retrieval by combining retrieval mechanisms with generative models, enabling more accurate and contextually relevant insights.
- Prompting Techniques like [Tree-of-Thought Prompting](https://arxiv.org/pdf/2305.10601) to facilitates complex reasoning processes to improve the quality of generated responses.
- Secure Data Handling: Protects sensitive information by identifying and masking personal data (e.g., names, document numbers) before any transmission to external services, ensuring confidentiality and compliance. (*coming soon*)

### Integration

- Apache Tika Integration: Efficiently extracts and processes information from a wide variety of document formats, ensuring versatile data handling.
- Redis Vector Database: Employs Redis for high-performance vector storage and retrieval, optimizing data management and access speeds.


### Documentation

The documentation was created using the `mkdocs-material` and `mkdocs-string` libraries.

```
https://andrecorumba.github.io/inspector/
```

## Libraries Used

This project leverages the following Python libraries and tools:
- python-dotenv: For environment variable management.
- openai: For interaction with Azure OpenAI’s GPT models.
- numpy: For numerical operations.
- langchain-text-splitters: For efficient text chunking.
- pytest: For testing.
- tiktoken: For tokenizing text for LLM interactions.
- fastapi: For building the backend REST API.
- uvicorn: ASGI server for FastAPI.
- streamlit: For building the frontend interface.
- streamlit-option-menu: For adding navigation menus to Streamlit apps.
- redis: For caching and database operations.
- redisvl: Vector library for similarity search in Redis.
- tika: For extracting content from diverse document formats.
- aiohttp: For asynchronous HTTP requests.
- python-multipart: For handling file uploads.

## Infrastructure

The project uses Docker for deployment, and services are orchestrated using docker-compose. The following services are included:
1. FastAPI: Port: 8997
    - Backend REST API
2. Streamlit: Port: 8998
    - Frontend of the POC
3. Redis: Port: 8999
    - Data volume: redis-data-inspector
4. MkDocs: Port: 8996
    - Serves project documentation.
5. Tika: Port: 8995
    - Extracts information from documents.

## Azure OpenAI Integration

The project utilizes Azure OpenAI services for generating insights and embeddings. Ensure the following environment variables `.env` file are configured:

```env
# If you use Azure services
AZURE_OPENAI_API_KEY = "your_api_key_here"
OPENAI_API_TYPE = "azure"
AZURE_OPENAI_ENDPOINT = "https://your_azure_endpointservices.com/"
OPENAI_API_VERSION = "api_version"
AZURE_DEPLOYMENT = "your_azure_azure_chat_deployment_name"
AZURE_EMBEDDING_DEPLOYMENT = "your_azure_embedding_deployment_name"

# If you use Openai Services
OPENAI_API_KEY="your_api_key_here"
MODEL_NAME = "gpt-4o-mini" # e.g

# Services
API_HOST=fastapi
API_PORT=8000
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
STREAMLIT_PORT=8501
TIKA_SERVER_ENDPOINT='http://tika:9998/'
```

These environment variables enable seamless interaction with Azure OpenAI endpoints for document analysis and embedding operations.

## How to Run

1. Clone the repository and navigate to the project directory:

```
git clone https://github.com/andrecorumba/inspector.git
cd inspector
```

2. Ensure you have Docker and Docker Compose installed.
3. Build and start the services:

```
docker-compose up --build
```

4. Access the application:
- FastAPI Backend: http://localhost:8997
- Streamlit Frontend: http://localhost:8998
- MkDocs Documentation: http://localhost:8996

## Contributing

Feel free to submit issues or pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License.

Author: André Rocha
Version: 0.2.0

Let me know if there are additional details or edits you'd like!