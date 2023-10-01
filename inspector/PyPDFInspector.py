import os

from dotenv import load_dotenv, find_dotenv

import openai

from langchain.document_loaders.pdf import PyPDFLoader
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma


class PyPDFInspectot():
    def __init__ (self):
        '''Initialize the ChatAuditReport class.'''

        self.model_name = "gpt-3.5-turbo-16k"
        self.documents = None
        self.docs_splited = None
        self.chunk_size = 4000
        self.embeddings = None
        self.vector_db = None
    
    def load_pdf_report_from_path(self, path_to_pdf_report: str):
        '''Load PDF report.'''
        
        if os.path.isfile(path_to_pdf_report):
            loader = PyPDFLoader(path_to_pdf_report)
            self.documents = loader.load()
        else:
            raise FileNotFoundError("File not found. Please check the path to the PDF report.")
        return self.documents
    
    def load_pdf_folder(self, path_to_pdf_report):
        '''Load PDF folder.'''
        if os.path.isdir(path_to_pdf_report):
            loader = PyPDFDirectoryLoader(path_to_pdf_report)
            self.documents = loader.load()
        else:
            raise FileNotFoundError("Folder not found. Please check the path to the PDF folder.")
        return self.documents
    
    def split_documents_from_tiktoken_encoder(self):
        '''Split the documents from TikToken encoder.
        See https://python.langchain.com/docs/modules/data_connection/document_transformers/text_splitters/split_by_token 
        Default chunk_size from TextSplitter class are 4000 caracters.'''
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name=self.model_name
            )
        self.chunk_size = text_splitter._chunk_size
        self.docs_splited = text_splitter.split_documents(self.documents)
        return self.docs_splited
    
    def load_openai_enviroment(self):
        '''Load the OpenAI enviroment.
        Need OpenAI API key. Get it from https://platform.openai.com/account/api-keys'''
        _ = load_dotenv(find_dotenv())
        openai.api_key = os.environ['OPENAI_API_KEY']

    def create_openai_embeddings(self):
        '''Create the embeddings from OpenAI.'''
        self.load_openai_enviroment()
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=openai.api_key,
            chunk_size=self.chunk_size
            )

    def chroma_vector_db(self):
        '''Create the Chroma vector database.'''
        self.create_openai_embeddings()
        self.vector_db = Chroma.from_documents(
            documents=self.docs_splited,
            embedding=self.embeddings,
            collection_name="py_pdf_inspector_store"
            )
    



if __name__ == "__main__":
    '''Test the ChatAuditReport class.'''

    report = PyPDFInspectot()
    report.load_pdf_report_from_path("data/1497056.pdf")
    print("report: ", len(report.documents))
    print("Tamanho do documento na posição: ",len(report.documents[0].page_content))
    print("DOCUMENT LOADED \n", report.documents[0])
    print("\n\n")

    # reports_in_folder = ChatAuditReport()
    # reports_in_folder.load_pdf_folder("/Users/andreluiz/Downloads/inspector-examples/idenficar-riscos")
    # print("reports_in_folder: ", len(reports_in_folder.documents))

    report.split_documents_from_tiktoken_encoder()
    print("report splited: ", len(report.docs_splited))
    print("Tamanho do split do documento na posição: ",len(report.docs_splited[0].page_content))
    # print("DOCUMENT SPLITED \n", report.docs_splited)

    report.chroma_vector_db()

    print("report vector_db: ")


