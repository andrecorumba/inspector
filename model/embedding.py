from model.split_text import SplitText
from typing import List, Union, Iterable
import os

import numpy as np

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from openai import AzureOpenAI

class InspectorEmbeddings():
    """
    A class to generate and manage embeddings using Azure OpenAI for textual content.

    Attributes:
        client (AzureOpenAI): The AzureOpenAI client configured for embedding generation.
        embedding_float (list): The list of generated embeddings in float format.
        embedding_bytes (list): The list of generated embeddings in byte format.
        dimensions (int): The dimensionality of the generated embeddings.
        data_to_vectorstore (list): A list of dictionaries prepared for storing in a vector database.
    """
    def __init__(self):
        """
        Initializes the InspectorEmbeddings instance and configures the Azure OpenAI client.
        """
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
        )->list:
        """
        Creates embeddings for the given content using Azure OpenAI.

        Args:
            content (str): The textual content to generate embeddings for.
            dimensions (int): The number of dimensions for the embeddings. Defaults to 3072.
            file_name (str): The name of the file associated with the content. Defaults to "file_name".
            chunk_size (int): The maximum size of text chunks. Defaults to 8000.

        Returns:
            list: A list of embeddings in float format.
        
        Raises:
            RuntimeError: If there is an error during embedding creation.
        """
        self.text_splitted_list = SplitText(chunk_size).split_text(content)

        # Remove blank items
        text_list = [item for item in self.text_splitted_list if item]

        # Create embeddings with Azure OpenAI
        try:
            self.embedding = self.client.embeddings.create(
                input=text_list,
                model='text-embedding-3-large',
                dimensions=dimensions,
            )
        except Exception as e:
            raise RuntimeError(f"Error to create embeddings: {e}")
        
        self.embedding_float = [emb.embedding for emb in self.embedding.data]
        self.embedding_bytes = [np.array(emb, dtype=np.float32).tobytes() for emb in self.embedding_float]
        self.dimensions = len(self.embedding.data[0].embedding)
        self.text_list = text_list
        self.file_name = file_name

        return self.embedding_float
    
    def prepare_data(self)->list:
        """
        Prepares the embedding data for storage in a vector database.

        Returns:
            list: A list of dictionaries containing file information, section number, text, and embedding.
        """
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
