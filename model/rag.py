from model.embedding import Embeddings
from model.vector_redis import RedisVectorStore
from model.config_schema import AppConfig

# import asyncio

from redisvl.query import VectorQuery
from openai import AzureOpenAI
import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class RAGRedis():
    def __init__(
            self, 
            config: AppConfig, 
            redis_url: str,
            k: int = 6, 
            dimensions: int = 3072, 
            chunk_size: int = 8000,
        ) -> None:
        self.config = config
        self.k = k
        self.dimensions = dimensions
        self.context = ""
        self.response_json = ""
        self.redis_url = redis_url
        self.chunk_size = chunk_size

        # Configuração do cliente OpenAI para Azure
        self.client_chat = AzureOpenAI(
            api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version = os.getenv("OPENAI_API_VERSION"),
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment = os.getenv("AZURE_DEPLOYMENT"),
            )

        # Inicializa o RedisVectorStore e cria o esquema se necessário
        self.redis_vector_obj = RedisVectorStore(redis_url=self.redis_url)
        self.index = self.redis_vector_obj.create_schema(self.config, self.dimensions, overwrite=True)

    def similarity_search(self, query: str):
        self.query = query
        query_emb_obj = Embeddings()
        query_emb_obj.azure_create_embedding(self.query, self.dimensions, self.chunk_size) 

        query_object = VectorQuery(
            vector = query_emb_obj.embedding_float,
            vector_field_name = "embedding",
            return_fields = ["text", "file_name", "section"],
            num_results = self.k,
            )
        self.context = self.index.query(query_object)
        return self.context
    
    def rag(self, query: str, prompt: str):
        self.query = query
        self.prompt = prompt

        self.similarity_search(self.query)

        self.messages = [
            {
                "role": "system",
                "content": f"Você é um Auditor Interno Governamental.",
            },
            {
                "role": "user",
                "content": self.prompt + str(self.context),
            },
        ]
        
        completion = self.client_chat.chat.completions.create(
            model="gpt-4o-mini",  
            messages=self.messages
        )
        self.response = completion.choices[0].message.content
        self.response_json = completion.to_json()
        self.usage = completion.usage.to_json()
        
        return self.response

