import streamlit as st

import os

import openai

from dotenv import load_dotenv, find_dotenv

from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma

CHUNK_SIZE = 500

def processar_llm(pasta_do_trabalho):
    """
    Função para processar o LLM.

    Parâmetros:
    pasta_do_trabalho (str): Caminho absoluto para a pasta do trabalho.

    Retorno:
    None
    """
    
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ['OPENAI_API_KEY']

    # Carrega a pasta com os arquivos
    pasta_arquivos= os.path.join(pasta_do_trabalho, "files")
    
    with st.spinner("Processando LLM .... 💫"):
        # Carrega os documentos no LangChain - LOAD

        docs_splited = carrega_documento_pdf(pasta_arquivos)

        # Cria os embeddings - EMBED
        openai_embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key,
                                            chunk_size=CHUNK_SIZE,
                                            max_retries=10)

        # Vector Stores - STORE
        
        # Diretório persistente
        pasta_vectordb = os.path.join(pasta_do_trabalho, "vectordb")

        vector_db = Chroma.from_documents(documents=docs_splited,
                                        embedding=openai_embeddings,
                                        collection_name="langchain_store",
                                        persist_directory=pasta_vectordb)
        
        # Persiste no diretório
        vector_db.persist()
    
    st.success("LLM Processado com Sucesso! 🎉")
    st.markdown(f"### Clique em ANALISAR para visualizar os resultados.")

def carrega_documento_pdf(pasta_arquivos):
    """
    Função para carregar os documentos PDF.

    Parâmetros:
    pasta_arquivos (str): Caminho absoluto para a pasta dos arquivos.

    Retorno:
    docs_splited (list): Lista com os documentos divididos em pedaços menores.
    """
    
    # Carrega os documentos no LangChain - LOAD
    loader = PyPDFDirectoryLoader(pasta_arquivos)
    documents = loader.load()

    # Divide os documentos em pedaços menores - SPLIT
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(model_name="gpt-3.5-turbo-16k",
                                                                chunk_size=CHUNK_SIZE,
                                                                chunk_overlap=0)
    docs_splited = text_splitter.split_documents(documents)

    return docs_splited