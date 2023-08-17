import streamlit as st
from streamlit_option_menu import option_menu

import os

import json

import openai

from dotenv import load_dotenv, find_dotenv

from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# Importando módulos internos
import chave
import pastas
from prompts import FIRST_QUESTIONS_PROMPT, USER_QUESTIONS_PROMPT, RISK_IDENTIFIER_PROMPT

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

    pasta_arquivos = pastas.pega_pasta(usuario, chave_do_trabalho, 'files')
    
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
        pasta_vectordb = pastas.pega_pasta(usuario, chave_do_trabalho, 'vectordb')


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
    
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ['OPENAI_API_KEY']

    lista_respostas = []

    try:
        pasta_do_trabalho = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', usuario, option)
        pasta_vectordb = os.path.join(pasta_do_trabalho, 'vectordb')
        pasta_arquivos = os.path.join(pasta_do_trabalho, 'files')
        pasta_database = os.path.join(pasta_do_trabalho, "database")


        # RetrievalQA
        # llm = processing_llm_openai(temperature=0.0, model="gpt-3.5-turbo-16k")
        # llm = OpenAI(temperature=0.0, model_name="gpt-3.5-turbo-16k" )
        #QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        # Construtor do embedding
        openai_embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key,
                                            chunk_size=CHUNK_SIZE,
                                            max_retries=3)
        
        # Construtor do VectorDB a partir do banco persistente
        vector_db = Chroma(collection_name="langchain_store",
                           persist_directory=pasta_vectordb, 
                           embedding_function=openai_embeddings)


        # Q&A a partir do RetrievalQA
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vector_db.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt})
        
        # Processa a pregunta no modelo e retorna a resposta
        with st.spinner("Processando Pergunta .... 💫"):
            resposta = qa_chain({'query': query})
            
            if query == " ":
                query = "Perguntas Sugeridas na Pré-Análise:"
            
            st.write(f"{query}")     
            st.write(resposta['result'])
            st.json(resposta['source_documents'], expanded=False)

            dict_resposta = {'query': query, 
                             'result': resposta['result']}
                       
            salvar_em_json(dict_resposta, os.path.join(pasta_database, 'qa.json'))
            salvar_em_txt(dict_resposta, os.path.join(pasta_database, 'qa.txt'))
    
    except Exception as e:
        st.warning('Não há trabalhos para analisar. Por favor, carregue documentos.')
        return
    

def generate_first_questions(usuario, option):
    query = " "
    llm = processing_llm_openai(temperature=0.4, model="gpt-3.5-turbo-16k")
    pdf_analizer(usuario, option, query, llm, FIRST_QUESTIONS_PROMPT)
    

def user_questions(usuario, option, query):
    llm = processing_llm_openai(temperature=0.0, model="gpt-3.5-turbo-16k")
    pdf_analizer(usuario, option, query, llm, USER_QUESTIONS_PROMPT)


def risk_identifier(user, option, query):
    llm = processing_llm_openai(temperature=0.6, model="gpt-3.5-turbo-16k")
    pdf_analizer(user, option, query, llm, RISK_IDENTIFIER_PROMPT)


def salvar_em_json(dados, caminho_arquivo):
    ''' 
    Função que salva os dados em um arquivo JSON.

    Parâmetros:
    dados (dict): Dicionário com os dados a serem salvos.
    caminho_arquivo (str): Caminho do arquivo JSON.
    '''

    lista_respostas = []
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            lista_respostas = json.load(f)
    lista_respostas.append(dados)
    
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(lista_respostas, f, ensure_ascii=False, indent=4)

def salvar_em_txt(dados, caminho_arquivo):
    ''' 
    Função que salva os dados em um arquivo txt.

    Parâmetros:
    dados (dict): Dicionário com os dados a serem salvos.
    caminho_arquivo (str): Caminho do arquivo txt.
    '''
    
    with open(caminho_arquivo, 'a', encoding='utf-8') as f:
        f.write(f"Pergunta: {dados['query']}\n\n")
        f.write(f"Resposta: {dados['result']}\n\n")

def processing_llm_openai(temperature, model):
    return OpenAI(temperature=temperature, model_name=model)