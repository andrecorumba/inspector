from model.embedding import InspectorEmbeddings
from model.vector_redis import RedisVectorStore
from model.config_schema import AppConfig

# import asyncio

from redisvl.query import VectorQuery
from openai import AzureOpenAI, OpenAI
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
            service: str = "azure"
        ) -> None:
        self.config = config
        self.k = k
        self.dimensions = dimensions
        self.context = ""
        self.response_json = ""
        self.redis_url = redis_url
        self.chunk_size = chunk_size
        self.client_chat = None
        self.service = service

        # Inicialize the Redis Vector
        self.redis_vector_obj = RedisVectorStore(redis_url=self.redis_url)
        self.index = self.redis_vector_obj.create_schema(self.config, self.dimensions, overwrite=True)

    def similarity_search(self, query: str):
        self.query = query
        query_emb_obj = InspectorEmbeddings()
        query_emb_obj.create_embedding(
            content=self.query, 
            dimensions=self.dimensions, 
            chunk_size=self.chunk_size,
            service=self.service
            ) 

        query_object = VectorQuery(
            vector = query_emb_obj.embedding_float,
            vector_field_name = "embedding",
            return_fields = ["text", "file_name", "section"],
            num_results = self.k,
            )
        self.context = self.index.query(query_object)
        return self.context
    
    def rag(self, query: str, prompt: str):
        """Standard RAG technique"""
        self.query = query
        self.prompt = prompt

        self.similarity_search(self.query)

        self.messages = [
            {
                "role": "system",
                "content": f"You are a specialist in document analysis.",
            },
            {
                "role": "user",
                "content": self.prompt.format_map(
                    {
                        "context" : str(self.context),
                        "language" : self.config.language
                    }
                    ),
            },
        ]
        
        try: 
            if self.service == "azure":
                self.client_chat = AzureOpenAI(
                    api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
                    api_version = os.getenv("OPENAI_API_VERSION"),
                    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
                    azure_deployment = os.getenv("AZURE_DEPLOYMENT"),
                    )
            
            elif self.service == "openai":
                self.client_chat = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))       
            
            completion = self.client_chat.chat.completions.create(
                model=os.getenv("MODEL_NAME"),  
                messages=self.messages,
            )
        except Exception as e:
            raise RuntimeError(f"Error to create chat: {e}")
        
        self.response = completion.choices[0].message.content
        self.response_json = completion.to_json()
        self.usage = completion.usage.to_json()
        
        return self.response
