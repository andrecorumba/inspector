FROM python:3.11-slim

WORKDIR /app

# Copia os arquivos de configuração do Poetry
COPY pyproject.toml poetry.lock ./
COPY .env ./

RUN python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

COPY model/ /app/model/
COPY view/ /app/view/
COPY controller/ /app/controller/
COPY data/ /app/data/

EXPOSE 8501

CMD ["streamlit", "run", "view/app.py", "--server.port=8501", "--server.address=0.0.0.0"]