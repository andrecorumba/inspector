# Inspector

Inspector is a Proof of Concept (POC) for a Python-based web application designed to analyze documents using cutting-edge AI technologies.

## Key Features

- **Insight Extraction**: Leverages large language models (LLMs) for user-driven document analysis, integrated with Azure OpenAI services.
- **Data Privacy**: Securely handles sensitive data by identifying and masking personal information (e.g., names, document numbers) before transmission to external services.
- **Backend and Frontend Integration**:
  - Backend: Powered by **FastAPI**.
  - Frontend: Built with **Streamlit**.
- **Tooling**:
  - **Redis** as a vector database for efficient data retrieval.
  - **Apache Tika** for extracting information from diverse document formats.
- **Advanced AI Techniques**:
  - **Retrieval-Augmented Generation (RAG)**.
  - Advanced prompting strategies like **Chain-of-Thought** and **Tree-of-Thought**.

## Azure OpenAI Integration

The project utilizes Azure OpenAI services for generating insights and embeddings. Ensure the following environment variables are configured:

```env
AZURE_OPENAI_API_KEY="xxxxx"
OPENAI_API_TYPE="azure"
AZURE_OPENAI_ENDPOINT="xxxxx"
OPENAI_API_VERSION="xxxxx"
AZURE_DEPLOYMENT="xxxxx"  # e.g., gpt-4o-mini
AZURE_EMBEDDING_DEPLOYMENT="xxxxx"

# Other Services Configuration
API_HOST=fastapi
API_PORT=8000
REDIS_HOST=redis
REDIS_PORT=6379
STREAMLIT_PORT=8501
TIKA_SERVER_ENDPOINT="http://tika:9998/"
```

These environment variables enable seamless interaction with Azure OpenAI endpoints for document analysis and embedding operations.

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