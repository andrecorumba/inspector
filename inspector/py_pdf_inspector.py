import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from dotenv import load_dotenv, find_dotenv

import openai

from langchain.document_loaders.pdf import PyPDFLoader
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate

# Import internal modules
import inspector.prompts as prompts


class PyPDFInspector():
    def __init__ (
            self, 
            model_name = "gpt-3.5-turbo-16k",
            temperature = 1.1,
            chunk_size = 4000
            ):
        '''Initialize the ChatAuditReport class.'''
        self.model_name = model_name 
        self.documents = None
        self.docs_splited = None
        self.chunk_size = chunk_size
        self.embeddings = None
        self.vector_db = None
        self.prompt = None
        self.llm = None
        self.temperature = temperature
        self.qa_chain = None
        self.response = None

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
    
    def openai_llm(self):
        '''Create the OpenAI LLM.'''
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo-16k", 
            temperature=self.temperature,
            max_tokens=4052
            )
        
    def azure_openai_llm(self):
        '''Create Azure OpenAI LLM.'''
        self.llm = AzureChatOpenAI(
            model="gpt-3.5-turbo-16k", 
            temperature=self.temperature,
            openai_api_version='2023-05-15',
            deployment_name='Teste-16k',
            max_tokens=4052
            )
    
    def load_prompt_template(self, prompt_template=None):
        '''Load the prompt template.'''
        if prompt_template == None:
            prompt_template = """
            A partir de trechos do documento pdf e responda a pergunta do usuário.
            Contexto: {context}
            Pergunta: {question}"""
        self.prompt = PromptTemplate.from_template(prompt_template)
        return self.prompt
    
    def retrieval_qa_chain(self):
        '''Create the Retrieval QA chain.'''
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vector_db.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt})
        return self.qa_chain
    
    def inspector_qa_chains(self, query):
        self.response = self.qa_chain({'query': query})
        return self.response
    
    def run_pdf_inspector_from_folder(
            self, 
            file_path: str, 
            model_name=None, 
            temperature=None,
            prompt_template=None
            ):
        '''Run the PDF inspector.'''
        if model_name is not None:
            self.model_name = model_name
        if temperature is not None:
            self.temperature = temperature
        if prompt_template is not None:
            self.prompt_template = temperature
        try:
            self.load_pdf_folder(file_path)
            self.split_documents_from_tiktoken_encoder()
            self.chroma_vector_db()
            self.openai_llm()
            self.load_prompt_template(prompt_template)
            self.retrieval_qa_chain()
        except Exception as e:
            print(f"An error occurred during PDF inspection: {str(e)}")
        
if __name__ == "__main__":
    '''Test the PyPDFInspector class.''' 
    report = PyPDFInspector()
    report.run_pdf_inspector_from_folder("data")

    query = "Qual a Unidade Auditada?"
    response  = report.inspector_qa_chains(query)
    
    print("report vector_db:", response)

