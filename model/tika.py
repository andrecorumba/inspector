import tika
from tika import parser
import hashlib

class TikaParser:
    """
    A class for parsing content from files and file bytes using Apache Tika.

    Attributes:
        tika_server (str): The endpoint for the Tika server. Defaults to 'http://localhost:8002/'.
    """

    def __init__(self, tika_server: str = 'http://localhost:8002/') -> None:
        """
        Initializes the TikaParser instance with a Tika server endpoint and starts the Tika Java Virtual Machine.

        Args:
            tika_server (str): The endpoint for the Tika server. Defaults to 'http://localhost:8002/'.
        """
        self.tika_server = tika_server
        tika.initVM()

    def tika_parser_from_bytes(self, file_binary: bytes) -> str:
        """
        Parses the content of a file provided as bytes using the Tika server.

        Args:
            file_binary (bytes): The binary content of the file to parse.

        Returns:
            str: The parsed content of the file.
        """
        parsed = parser.from_buffer(string=file_binary, serverEndpoint=self.tika_server)
        self.content = parsed["content"]
        return self.content

    def tika_parser_from_file_path(self, file_path: str) -> str:
        """
        Parses the content of a file provided via file path using the Tika server.

        Args:
            file_path (str): The path to the file to parse.

        Returns:
            str: The parsed content of the file.
        """
        parsed = parser.from_file(filename=file_path, serverEndpoint=self.tika_server)
        self.content = parsed["content"]
        return self.content

    def hash_file_bytes(self, file_bytes: bytes) -> str:
        """
        Generates a SHA-256 hash for the given file bytes.

        Args:
            file_bytes (bytes): The binary content of the file to hash.

        Returns:
            str: The SHA-256 hash of the file content.
        """
        sha256_hash = hashlib.sha256()
        sha256_hash.update(file_bytes)
        return sha256_hash.hexdigest()
