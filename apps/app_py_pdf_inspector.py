import streamlit as st
import os
import random
import string

from streamlit_option_menu import option_menu

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from inspector.py_pdf_inspector import PyPDFInspector

from inspector import (
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
            report.load_persistent_chroma_vector_db_and_retrieval(
                file_path=os.path.join(user_folder,option_work)
                )    
            report.prompt = prompts.USER_QUESTIONS_PROMPT
            report.inspector_qa_chains(query=query)
            st.write(report.response)

# def process_files(temp_folder):
#     # temp_folder = create_temporary_folder()
#     # file_list_save_path = save_all_files(
#     #     temp_folder, 
#     #     uploaded_files
#     #     )
#     # st.success(f"Arquivos Carregados: {file_list_save_path}") 
    
#     # report = PyPDFInspector()
#     global report
#     report.run_pdf_inspector_from_folder(temp_folder)
    
#     st.success("Arquivos Processados com Sucesso! ✅")

# def input_question():
#     '''Input question to the report.'''
#     global report
#     query = st.text_input("Pergunta:", "Qual a Unidade Auditada?")
#     submitted = st.button("Enviar", key="button_submit")      
#     if submitted:
#         response = report.inspector_qa_chains(query=query)
#         st.write(response)

#         # st.button("Sair", key="button_exit")
#         # if st.session_state["button_exit"]:
#         #     delete_temp_folder(temp_folder)
#         #     st.success("Saindo do Relatório ... ✅")

# def upload_files():
#     uploaded_files = st.file_uploader(
#         label="Carregue o Relatório", 
#         type=["pdf"], 
#         key='upload_report',
#         accept_multiple_files=True,
#         )
#     return uploaded_files

# def create_temporary_folder():
#     """Create a temporary folder with unique code to store the uploaded files."""
#     combination = ''.join(random.choice(string.digits) for _ in range(6))
#     temp_folder = os.path.join("temporary", f"temp_{combination}")
#     if not os.path.exists(temp_folder):
#         os.mkdir(temp_folder)
#     return temp_folder

# def delete_temp_folder(temp_folder):
#     """Delete the temporary folder."""
#     if os.path.exists(temp_folder):
#         os.rmdir(temp_folder)
#     return temp_folder

# def save_all_files(temp_folder, file_list):
#     file_list_save_path = []
#     for file in file_list:
#         with open(os.path.join(temp_folder, file.name),"wb") as f:
#             f.write((file).getbuffer())
#         file_list_save_path.append(os.path.join(temp_folder, file.name))
#     return file_list_save_path


if __name__ == "__main__":
    app('user')