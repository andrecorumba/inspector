from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List


class SplitText:
    """
    A utility class for splitting large text into smaller chunks using
    the RecursiveCharacterTextSplitter from the langchain_text_splitters library.

    Attributes:
        chunk_size (int): Maximum size of each text chunk. Defaults to 8000.
    """

    def __init__(self, chunk_size: int = 8000) -> None:
        """
        Initializes the SplitText instance with a specified chunk size.

        Args:
            chunk_size (int): Maximum size of each chunk. Defaults to 8000.
        """
        self.chunk_size = chunk_size

    def split_text(self, content: str) -> List[str]:
        """
        Splits the given text into smaller chunks using RecursiveCharacterTextSplitter.

        Args:
            content (str): The input text to be split.

        Returns:
            List[str]: A list of text chunks.
        
        Raises:
            ValueError: If the content is not a valid string.
        """
        if not isinstance(content, str):
            raise ValueError("The 'content' parameter must be a string.")
        
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size, chunk_overlap=0
        )
        return splitter.split_text(content)
    

    # def split_tiktoken(self, content: str)->List[str]:

    #     # Muda e chamar o split da SETENCE TRANSFORMERS

    #     enc = tiktoken.get_encoding("cl100k_base")
    #     final_text_list = []
    #     cleaned_text_list = self._clean_text(content)

    #     def split_into_chunks(item, chunk_size):
    #         tokens = self._encode_text(item)
    #         return [tokens[i:i + chunk_size] for i in range(0, len(tokens), chunk_size)]
        
    #     for item in cleaned_text_list:
    #         len_item_tokens = len(self._encode_text(item))
            
    #         if len_item_tokens < self.chunk_size:
    #             final_text_list.append(self._encode_text(item))
    #         else:
    #             chunks = split_into_chunks(item, self.chunk_size)
    #             final_text_list.extend(chunks)
        
    #     text_splitted_list = [enc.decode(item) for item in final_text_list]

    #     self.text_splitted_list = self._group_paragraphs_list_in_chunck_size(text_splitted_list)

    #     return self.text_splitted_list

    # def _clean_text(self, content: str)->list:
    #     paragraphs = content.split('\n\n')
    #     cleaned_text_list = []
    #     for item in paragraphs:
    #         if item != '':
    #             item = item.strip()
    #             item = item.replace('\\n', '\n').replace('\\t', '\t')
    #             cleaned_text_list.append(item)
    #     return cleaned_text_list

    # def _encode_text(self, text: str):
    #     """Split documents"""
    #     enc = tiktoken.get_encoding("cl100k_base")
    #     text_encoded = enc.encode(text)
    #     return text_encoded
    
    # def _decode_text(self, encoded_text: List[str])->List[str]:
    #     enc = tiktoken.get_encoding("cl100k_base")
    #     decoded_text = enc.decode(encoded_text)
    #     return decoded_text
    
    # def _group_paragraphs_list_in_chunck_size(self, text_splitted_list: list):
    #     """Agrupa a lista em lista com varários parágrafos até o tamanho do chunck size"""
    #     if text_splitted_list:
    #         merged_list = []
    #         temp = []

    #         for sublist in text_splitted_list:
    #             item = sublist 
    #             if len(''.join(temp) + item) <= self.chunk_size:
    #                 temp.append(item)
    #             else:
    #                 merged_list.append(''.join(temp))  
    #                 temp = [item]

    #         # Add any remaining accumulated items to the final list
    #         if temp:
    #             merged_list.append(''.join(temp))

    #         return merged_list
