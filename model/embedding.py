from model.split_text import SplitText
from typing import List, Union, Iterable
import os

import numpy as np

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from openai import AzureOpenAI

class Embeddings():
    def __init__(self):
        self.client = AzureOpenAI(
            api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version = os.getenv("OPENAI_API_VERSION"),
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment = os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
        )
        self.embedding_float = None
        self.embedding_bytes = None
        self.dimensions = None
        self.data_to_vectorstore = []

    def azure_create_embedding(
            self, 
            content: str,
            dimensions: int = 3072,
            file_name: str = "file_name",
            chunk_size: int = 8000,
            ):
        
        self.text_splitted_list = SplitText(chunk_size).split_tiktoken(content)

        # Remove itens vazios da lista
        text_list = [item for item in self.text_splitted_list if item]

        # Gera os embeddings com Azure OpenAI
        try:
            self.embedding = self.client.embeddings.create(
                input=text_list,
                model='text-embedding-3-large',
                dimensions=dimensions,
            )
        except Exception as e:
            raise RuntimeError(f"Erro ao criar embeddings: {e}")
        
        self.embedding_float = [emb.embedding for emb in self.embedding.data]
        self.embedding_bytes = [np.array(emb, dtype=np.float32).tobytes() for emb in self.embedding_float]
        self.dimensions = len(self.embedding.data[0].embedding)
        self.text_list = text_list
        self.file_name = file_name

        return self.embedding_float
    
    def prepare_data(self):
        """Prepare data to Vector Store"""
        for i, text in enumerate(self.text_list):
            self.data_to_vectorstore.append(
                {
                    "file_name": self.file_name,
                    "section": i+1,
                    "text": text,
                    "embedding": self.embedding_bytes[i],
                } 
            )
        return self.data_to_vectorstore
