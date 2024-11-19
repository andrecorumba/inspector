from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

class SplitText:
    """
    A utility class for splitting large text into smaller chunks using
    the RecursiveCharacterTextSplitter from the langchain_text_splitters library.

    Attributes:
        chunk_size (int): The maximum size of each text chunk. Defaults to 8000.
    """

    def __init__(self, chunk_size: int = 8000) -> None:
        """
        Initializes the SplitText instance with a specified chunk size.

        Args:
            chunk_size (int): The maximum size of each text chunk. Defaults to 8000.
        """

        self.chunk_size = chunk_size

    def split_text(self, content: str) -> List[str]:
        """
        Splits the given text into smaller chunks using RecursiveCharacterTextSplitter.

        Args:
            content (str): The text content to split into chunks.

        Returns:
            List[str]: A list of text chunks.
        """

        if not isinstance(content, str):
            raise ValueError("The 'content' parameter must be a string.")
        
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size, chunk_overlap=0
        )
        return splitter.split_text(content)
    