from redisvl.index import SearchIndex


from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from model.embedding import Embeddings

from model.config_schema import AppConfig


class RedisVectorStore():
    def __init__(self, redis_url) -> None:
        self.redis_url = redis_url
        self.index = None
        self.keys = None
        self.info = None

    def load_data(self, emb_obj: Embeddings, config: AppConfig):
        if emb_obj != None:
            data_to_vectorstore = emb_obj.data_to_vectorstore
            dimensions = emb_obj.dimensions
            self.create_schema(config, dimensions)
            self.keys = self.index.load(data_to_vectorstore)
            return self.keys

    def create_schema(self, config: AppConfig, dimensions: int = 3072, overwrite: bool = True):
        """Create a Redis Schema."""
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