# Import External Modules
import streamlit as st
from streamlit_option_menu import option_menu

import os

import openai
import shutil

from dotenv import load_dotenv, find_dotenv

from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders.pdf import PyPDFDirectoryLoader
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document
from langchain.callbacks import get_openai_callback

# Import Local Modules
from prompts import RISK_IDENTIFIER_PROMPT, REFINE_PROMPT_RISKS
import pdf_inspector
import folders

CHUNK_SIZE_RISK = 10000
CHUNK_OVERLAP_RISK = 200

def risk_identifier_individual_file(user, option_work):
    # Get folders to work
    try:
        work_folder = folders.get_folder(user, option_work, 'work_folder')  
        files_folder = folders.get_folder(user, option_work, 'files')
        response_folder = folders.get_folder(user, option_work, 'responses')  
    except FileNotFoundError:
        st.error('Erro ao carregar as pastas de trabalho.')
        return
    
    # get all files in files_folder
    files = os.listdir(files_folder)

    for file in files:
        # LOAD -  Load the pdf documents
        loader = PyPDFLoader(os.path.join(files_folder, file))
        document = loader.load()

        # SPLIT - Split the documents into chunks
        documents_for_risk_gen = split_text_risk(str(document), 
                   chunk_size=CHUNK_SIZE_RISK, 
                   chunk_overlap=CHUNK_OVERLAP_RISK)

        # Initialize the LLM
        llm = pdf_inspector.init_llm_openai(temperature=1.1, model="gpt-3.5-turbo-16k")


        # Generate risk analysis
        risks_chain = load_summarize_chain(llm=llm, 
                                           chain_type="refine", 
                                           question_prompt=RISK_IDENTIFIER_PROMPT, 
                                           refine_prompt=REFINE_PROMPT_RISKS)
        with get_openai_callback() as cb:
            response_risk = risks_chain.run(documents_for_risk_gen)

        # Save the response
        with open(os.path.join(response_folder, f'risks_{file}.txt'), 'w') as f:
            f.write(f"Arquivo: {file}\n\nCustos: {cb}\n\nRiscos Identificados:\n\n{response_risk}\n\n")

    # Zip files in response folder
    zip_file = shutil.make_archive(option_work, 'zip', response_folder)
        
    return response_risk, cb, zip_file

def risks_identifier(user, option_work):
    """
    Function to identify risks in documents.

    Parameters:
    user (str): User name.
    option_work (str): Work key.

    Return:
    response_risk (str): Response from LLM.
    """
    
    # Load the API key
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ['OPENAI_API_KEY']


    # Get folders to work
    try:
        work_folder = folders.get_folder(user, option_work, 'work_folder')  
        files_folder = folders.get_folder(user, option_work, 'files')  
    except FileNotFoundError:
        st.error('Erro ao carregar as pastas de trabalho.')
        return
    
    try:
        # LOAD -  Load the pdf documents
        loader = PyPDFDirectoryLoader(files_folder)
        documents = loader.load()

        files_loaded = documents[0].metadata['source']

        # SPLIT - Split the documents into chunks
        documents_for_risk_gen = split_text_risk(str(documents), 
                   chunk_size=CHUNK_SIZE_RISK, 
                   chunk_overlap=CHUNK_OVERLAP_RISK)

        # Initialize the LLM
        llm = pdf_inspector.init_llm_openai(temperature=1.1, model="gpt-3.5-turbo-16k")


        # Generate risk analysis
        risks_chain = load_summarize_chain(llm=llm, 
                                           chain_type="refine", 
                                           question_prompt=RISK_IDENTIFIER_PROMPT, 
                                           refine_prompt=REFINE_PROMPT_RISKS)
        with get_openai_callback() as cb:
            response_risk = risks_chain.run(documents_for_risk_gen)
        
        return response_risk, cb, files_loaded
    
    except Exception as e:
        st.error('Erro ao processar LLM.', e)
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