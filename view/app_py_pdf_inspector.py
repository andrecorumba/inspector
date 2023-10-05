import streamlit as st
import os
import random
import string

from streamlit_option_menu import option_menu

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from model.py_pdf_inspector import PyPDFInspector

from controller import (
    folders,
    prompts)

def app(user):
    user_work_list = []
    user_folder = folders.get_folder(
            user=user,
            work_key='todos',
            type_of_folder='user_folder'
            )
    for item in os.listdir(user_folder):
        if not item.startswith('.'):
            user_work_list.append(item)

    with st.sidebar:
        option_work = st.selectbox(
            label="Lista de Trabalhos",
            options=user_work_list
            )
        st.write('Você Selecionou:', option_work)
        st.radio('Selecione', options=[# 'Mostrar Histório',
                                        'Fazer Minhas Perguntas',
                                        'Gerar Perguntas Prontas',], 
                                        key='radio_show_questions')
        
    if st.session_state['radio_show_questions'] == 'Fazer Minhas Perguntas':
        if query:=st.text_input("Digite sua pergunta:"):  
            report = PyPDFInspector()
            
            report.prompt = prompts.PORTUGUESE_BASIC_PROMPT
            report.load_persistent_chroma_vector_db_and_retrieval(
                persistent_folder=os.path.join(
                    user_folder,
                    option_work, 
                    'vectordb',
                    ),
                )    
            report.inspector_qa_chains(query=query)
            st.write(report.response)
    
    elif st.session_state['radio_show_questions'] == 'Gerar Perguntas Prontas':
            first_questions = PyPDFInspector(
                 temperature=0.3
                 )
            first_questions.prompt = prompts.FIRST_QUESTIONS_PORTUGUESE_PROMPT
            first_questions.load_persistent_chroma_vector_db_and_retrieval(
                persistent_folder=os.path.join(
                    user_folder,
                    option_work, 
                    'vectordb',
                    ),
                )    
            first_questions.inspector_qa_chains(query=' ')
            st.write(first_questions.response)


if __name__ == "__main__":
    app('user')