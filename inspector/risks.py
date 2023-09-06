# Import External Modules
import streamlit as st
from streamlit_option_menu import option_menu

import os
import sys 
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import openai
import shutil

from dotenv import load_dotenv, find_dotenv

from langchain.llms import OpenAI
from langchain.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.callbacks import get_openai_callback

# Import Local Modules
from inspector.prompts import RISK_IDENTIFIER_PROMPT, REFINE_PROMPT_RISKS
from inspector import folders

CHUNK_SIZE_RISK = 10000
CHUNK_OVERLAP_RISK = 200

def risk_identifier_individual_file(user, work_key, text_input_openai_api_key):
    # Get folders to work
    work_folder = folders.get_folder(user, work_key, 'work_folder')  
    upload_folder = folders.get_folder(user, work_key, 'upload')
    response_folder = folders.get_folder(user, work_key, 'responses')  
    download_folder = folders.get_folder(user, work_key, 'download')

    # To use LLM OpenAI uncomment the line below
    openai.api_key = get_api_key(text_input_openai_api_key)
    llm = OpenAI(temperature=1.1, model_name="gpt-3.5-turbo-16k", openai_api_key=openai.api_key)
    
    # get all files in files_folder
    files = os.listdir(upload_folder)

    for file in files:
        # LOAD -  Load the pdf documents
        loader = PyPDFLoader(os.path.join(upload_folder, file))
        document = loader.load()

        # SPLIT - Split the documents into chunks
        documents_for_risk_gen = split_text_risk(str(document), 
                   chunk_size=CHUNK_SIZE_RISK, 
                   chunk_overlap=CHUNK_OVERLAP_RISK)

        # Generate risk analysis
        risks_chain = load_summarize_chain(llm=llm, 
                                           chain_type="refine", 
                                           question_prompt=RISK_IDENTIFIER_PROMPT, 
                                           refine_prompt=REFINE_PROMPT_RISKS)
        with get_openai_callback() as cb:
            response_risk = risks_chain.run(documents_for_risk_gen)

        # Save the response
        save_file(response_folder, file, work_key, response_risk, cb)

    # Zip files in response folder
    zip_file = shutil.make_archive(os.path.join(download_folder, work_key), 'zip', root_dir=response_folder)
        
    return response_risk, cb, zip_file

    
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

def save_file(response_folder, file, work_key, response_risk, cb):
    with open(os.path.join(response_folder, f'risks_{file}.txt'), 'w') as f:
        file_content = f"""Chave do Trabalho:{work_key}
        Arquivo: {file}
        Custos: {cb}
        Riscos Identificados:
        {response_risk}"""

        f.write(file_content)

def get_api_key(text_input_openai_api_key: str):

    if text_input_openai_api_key == 'openai':
        _ = load_dotenv(find_dotenv())
        api_key = os.environ['OPENAI_API_KEY']
    
    else:
        api_key = text_input_openai_api_key

    return api_key