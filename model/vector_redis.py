from redisvl.index import SearchIndex


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from model.embedding import InspectorEmbeddings

from model.config_schema import AppConfig


class RedisVectorStore():
    """
    A class for managing a vector store in Redis, including loading data and creating schemas for embeddings.

    Attributes:
        redis_url (str): The URL for connecting to the Redis instance.
        index (SearchIndex): The Redis search index instance.
        keys (list): The keys loaded into the Redis vector store.
        info (dict): Information about the current Redis search index.
    """

    def __init__(self, redis_url) -> None:
        """
        Initializes the RedisVectorStore instance with a Redis URL.

        Args:
            redis_url (str): The Redis connection URL.
        """

        self.redis_url = redis_url
        self.index = None
        self.keys = None
        self.info = None

    def load_data(self, emb_obj: InspectorEmbeddings, config: AppConfig) -> list:
        """
        Loads data from an embedding object into the Redis vector store.

        Args:
            emb_obj (InspectorEmbeddings): The embeddings object containing vector data and dimensions.
            config (AppConfig): The application configuration object.

        Returns:
            list: A list of keys corresponding to the loaded data in the Redis store.
        """

        if emb_obj != None:
            data_to_vectorstore = emb_obj.data_to_vectorstore
            dimensions = emb_obj.dimensions
            self.create_schema(config, dimensions)
            self.keys = self.index.load(data_to_vectorstore)
            return self.keys

    def create_schema(self, config: AppConfig, dimensions: int = 3072, overwrite: bool = True) -> SearchIndex:
        """
        Creates a schema in Redis for storing document embeddings.

        Args:
            config (AppConfig): The application configuration object.
            dimensions (int): The number of dimensions for the vector embeddings. Defaults to 3072.
            overwrite (bool): Whether to overwrite an existing schema. Defaults to True.

        Returns:
            SearchIndex: The Redis search index instance.

        """
        
        schema = {
            "index": {
                "name": f"document-index:{config.user}:{config.task_id}",
                "prefix": f"doc:{config.user}:{config.task_id}",
                "storage_type": "hash", 
            },
            "fields": [
                {
                    "name": "file_name",
                    "type": "tag"
                },
                {
                    "name": "section",
                    "type": "tag"
                },
                {
                    "name": "text", 
                    "type": "text"
                },
                {
                    "name": "embedding",
                    "type": "vector",
                    "attrs": {
                        "dims": dimensions,
                        "distance_metric": "cosine",
                        "algorithm": "flat",
                        "datatype": "float32",
                    }
                },
            ],
        }
        self.index = SearchIndex.from_dict(schema)
        self.index.connect(self.redis_url)
        self.index.create(overwrite=overwrite)
        self.info = self.index.info()
        return self.index