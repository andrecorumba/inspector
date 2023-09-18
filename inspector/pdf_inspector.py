# Import External Modules
import streamlit as st
from streamlit_option_menu import option_menu

import os

import sqlite3

import json

import openai

import tiktoken

from dotenv import load_dotenv, find_dotenv

from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.callbacks import get_openai_callback

# Import internal modules
from inspector import folders
from inspector.prompts import FIRST_QUESTIONS_PROMPT, USER_QUESTIONS_PROMPT

CHUNK_SIZE = 500

def pdf_load_split_vector(usuario, chave_do_trabalho):
    """
    Função que executa os passos de Load, Embedding e VectorDB do LangChain.
    Lê os arquivos PDF da pasta de trabalho, divide em partes menores e cria o VectorDB.

    Parâmetros:
    usuario (str): Nome do usuário.
    chave_do_trabalho (str): Chave do trabalho.

    Retorno:
    None
    """
    
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ['OPENAI_API_KEY']

    pasta_arquivos = folders.get_folder(usuario, chave_do_trabalho, 'upload')
    
    with st.spinner("Processando LLM .... 💫"):
        
        # LOAD -  Carrega os arquivos pdf
        loader = PyPDFDirectoryLoader(pasta_arquivos)
        documents = loader.load()


        # SPLIT - Divide os documentos em pedaços menores
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(model_name="gpt-3.5-turbo-16k",
                                                                    chunk_size=CHUNK_SIZE,
                                                                    chunk_overlap=0)
        docs_splited = text_splitter.split_documents(documents)

        # EMBEDDING - Cria os embeddings
        openai_embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key,
                                            chunk_size=CHUNK_SIZE,
                                            max_retries=3)


        # Diretório persistente
        pasta_vectordb = folders.get_folder(usuario, chave_do_trabalho, 'vectordb')


        # VECTOR_DB - Cria o VectorDB
        vector_db = Chroma.from_documents(documents=docs_splited,
                                        embedding=openai_embeddings,
                                        collection_name="langchain_store",
                                        persist_directory=pasta_vectordb)
        vector_db.persist()

def pdf_analizer(usuario, option, query, llm, prompt):
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


    try:
        work_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', usuario, option)
        vectordb_folder = os.path.join(work_folder, 'vectordb')
        files_folder = os.path.join(work_folder, 'files')
        database_folder = os.path.join(work_folder, "database")
    except FileNotFoundError:
        st.warning('Não há trabalhos para analisar. Por favor, carregue documentos.')
        return
    
    try:
        # Embedding constructor
        openai_embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key,
                                            chunk_size=CHUNK_SIZE,
                                            max_retries=3)
        
        # VectorDB constructor from the persistent database
        vector_db = Chroma(collection_name="langchain_store",
                           persist_directory=vectordb_folder, 
                           embedding_function=openai_embeddings)
        
        # Q&A from RetrievalQA
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vector_db.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt})

        with st.spinner("Processando Pergunta .... 💫"):
            resposta = qa_chain({'query': query})
            if query == " ":
                query = "Perguntas Sugeridas na Pré-Análise:"
            st.write(f"{query}")     
            st.write(resposta['result'])
            st.json(resposta['source_documents'], expanded=False)
            dict_resposta = {'query': query, 
                             'result': resposta['result']}
                       
            #save_in_json(dict_resposta, os.path.join(database_folder, 'qa.json'))
            # save_in_txt(dict_resposta, os.path.join(database_folder, 'qa.txt'))

            return dict_resposta['result']
    
    except Exception as e:
        st.warning('Erro ao processar LLM.')
        return
    
def generate_first_questions(usuario, option):
    # Load the API key
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ['OPENAI_API_KEY']
    
    query = " "
    llm = init_llm_openai(temperature=0.4, model="gpt-3.5-turbo-16k")
    first_questions = pdf_analizer(usuario, option, query, llm, FIRST_QUESTIONS_PROMPT)   
    return first_questions 

def user_questions(usuario, option, query):
    # Load the API key
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ['OPENAI_API_KEY']
    #
    llm = init_llm_openai(temperature=0.0, model="gpt-3.5-turbo-16k")
    pdf_analizer(usuario, option, query, llm, USER_QUESTIONS_PROMPT)


def save_in_json(data: dict, file_path: str):
    ''' 
    Função que salva os dados em um arquivo JSON.

    Parâmetros:
    dados (dict): Dicionário com os dados a serem salvos.
    caminho_arquivo (str): Caminho do arquivo JSON.
    '''

    lista_respostas = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            lista_respostas = json.load(f)
    lista_respostas.append(data)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(lista_respostas, f, ensure_ascii=False, indent=4)

def save_in_txt(data: dict, file_path: str):
    ''' 
    Função que salva os dados em um arquivo txt.

    Parâmetros:
    dados (dict): Dicionário com os dados a serem salvos.
    caminho_arquivo (str): Caminho do arquivo txt.
    '''
    
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"Pergunta: {data['query']}\n\n")
        f.write(f"Resposta: {data['result']}\n\n")

def init_llm_openai(temperature, model):
    return OpenAI(temperature=temperature, model_name=model)

def count_prompt_tokens(prepareted_prompt):
    '''
    Function that counts the number of tokens in the prompt.

    Parameters:
    prepareted_prompt (list): List of prepareted prompt.

    Return: 
    num_tokens (int): Number of tokens in the prompt.
    '''    
    
    # length_of_caracters = len(prepareted_prompt[0][0].text)
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo-16k')
    num_tokens = len(encoding.encode(prepareted_prompt[0][0].text))

    return num_tokens