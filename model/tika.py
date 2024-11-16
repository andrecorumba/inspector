import tika
from tika import parser
import hashlib

class TikaParser():
    def __init__(self, tika_server: str = 'http://localhost:8002/') -> None:
        self.tika_server = tika_server
        tika.initVM()

    def tika_parser_from_bytes(self, file_binary: bytes) -> str: 
        parsed = parser.from_buffer(string=file_binary, serverEndpoint=self.tika_server)
        self.content = parsed["content"]
        return self.content
    
    def tika_parser_from_file_path(self, file_path: str) -> str:
        parsed = parser.from_file(filename=file_path, serverEndpoint=self.tika_server)
        self.content = parsed["content"]
        return self.content
    
    def hash_file_bytes(self, file_bytes: bytes):
        """Função para gerar o hash SHA-256 a partir dos bytes de um arquivo."""
        sha256_hash = hashlib.sha256()
        sha256_hash.update(file_bytes)
        return sha256_hash.hexdigest()
