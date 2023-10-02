import streamlit as st
import os
import random
import string

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from inspector.py_pdf_inspector import PyPDFInspector

file_list_save_path = "temporary/temp_076839"
report = PyPDFInspector()  
report.run_pdf_inspector_from_folder(file_list_save_path)


def app():
    """App from py_pdf_inspector.py."""
    st.title("Converse com o Relatório")
    st.markdown("""Aqui você pode conversar com o relatório, 
                fazendo perguntas sobre o que você deseja saber.
                """)
    
    form_to_question(report)


def form_to_question(report):
    with st.form("my_form"):
        query = st.text_area("Pergunta:", "Qual a Unidade Auditada?")
        submitted = st.form_submit_button("Submit")
        if submitted:
            if report is not None:
                response = report.inspector_qa_chains(query)
                st.write(response)
            else:
                st.error("O objeto 'report' não foi inicializado corretamente.")

def upload_files():
    st.file_uploader(
        label="Carregue o Relatório", 
        type=["pdf"], 
        key='upload_report',
        accept_multiple_files=True,
        )

    if st.session_state["upload_report"] is not None:
        if st.button("Carregar Relatório"):
            temp_folder = create_temporary_folder()
            file_list_save_path = save_all_files(
                temp_folder, 
                st.session_state['upload_report']
                )
            st.success(f"Arquivos Carregados: {file_list_save_path}")
    return file_list_save_path

def create_temporary_folder():
    """Create a temporary folder with unique code to store the uploaded files."""
    combination = ''.join(random.choice(string.digits) for _ in range(6))
    temp_folder = os.path.join("temporary", f"temp_{combination}")
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
    return temp_folder

def delete_temp_folder(temp_folder):
    """Delete the temporary folder."""
    if os.path.exists(temp_folder):
        os.rmdir(temp_folder)
    return temp_folder

def save_all_files(temp_folder, file_list):
    file_list_save_path = []
    for file in file_list:
        with open(os.path.join(temp_folder, file.name),"wb") as f:
            f.write((file).getbuffer())
        file_list_save_path.append(os.path.join(temp_folder, file.name))
    return file_list_save_path


if __name__ == "__main__":
    app()