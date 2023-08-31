# Import External Modules
import streamlit as st
from streamlit_option_menu import option_menu

import os

import sqlite3

import json

import openai

import tiktoken

from dotenv import load_dotenv, find_dotenv

from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.chains.llm import LLMChain
from langchain.callbacks import get_openai_callback

# Import Local Modules
from prompts import RISK_IDENTIFIER_PROMPT, REFINE_PROMPT_RISKS
import pdf_inspector
import folders

CHUNK_SIZE_RISK = 10000
CHUNK_OVERLAP_RISK = 200

def risks_identifier(user, option):
    """
    Função que analisa arquivos PDF.

    Parâmetros:
    usuario (str): Nome do usuário.
    option (str): Opção de análise.
    query (str): Consulta.
    template (str): Template de consulta.

    Retorno:
    None
    """
    
    # Load the API key
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ['OPENAI_API_KEY']


    # Get folders to work
    try:
       
        work_folder = folders.get_folder(user, option, 'work_folder')  
        files_folder = folders.get_folder(user, option, 'files')  
    except FileNotFoundError:
        st.warning('Não há trabalhos para analisar. Por favor, carregue documentos.')
        return
    
    
    try:

        # LOAD -  Carrega os arquivos pdf
        loader = PyPDFDirectoryLoader(files_folder)
        documents = loader.load()

        # SPLIT - Divide os documentos em pedaços menores
        documents_for_risk_gen = split_text_risk(str(documents), 
                   chunk_size=CHUNK_SIZE_RISK, 
                   chunk_overlap=CHUNK_OVERLAP_RISK)

        # Initialize the LLM
        llm = pdf_inspector.init_llm_openai(temperature=0.0, model="gpt-3.5-turbo-16k")


        # Generate risk analysis
        risks_chain = load_summarize_chain(llm=llm, 
                                           chain_type="refine", 
                                           question_prompt=RISK_IDENTIFIER_PROMPT, 
                                           refine_prompt=REFINE_PROMPT_RISKS)

        response_risk = risks_chain.run(documents_for_risk_gen)
        
        return response_risk
    
    except Exception as e:
        st.warning('Erro ao processar LLM.', e)
        return
    
# Function to split text into chunks
def split_text_risk(text, chunk_size, chunk_overlap):
    # Initialize text splitter
    text_splitter = TokenTextSplitter(model_name="gpt-3.5-turbo-16k", 
                                      chunk_size=chunk_size, 
                                      chunk_overlap=chunk_overlap)

    # Split text into chunks
    text_chunks = text_splitter.split_text(text)

    # Convert chunks to documents
    documents = [Document(page_content=t) for t in text_chunks]

    return documents