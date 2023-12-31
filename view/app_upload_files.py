import streamlit as st
import sys
import os

from controller import folders, work_key
from model.py_pdf_inspector import PyPDFInspector

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def upload_files(
    type: list[str],
    type_of_work: str = 'report', 
    user: str = 'user') -> str:
    """Function to upload files to the user folder."""

    st.file_uploader(
        'Selecione os arquivos para análise', 
        type=type,
        accept_multiple_files=True,
        key='uploaded_file_list'
        )
    
    if st.session_state['uploaded_file_list'] is not None:
        if st.button('Processar Arquivos'):
            user_folder = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                '..',
                'data',
                user
                )
            key = work_key.create_key(type_of_work)
            
            # Create and get folders to work
            folders.create_folders(user_folder, key)
            files_folder = folders.get_folder(user, key, 'upload')
            vectordb_folder = folders.get_folder(user, key, 'vectordb')
                        
            for file in st.session_state['uploaded_file_list']:
                with open(os.path.join(files_folder, file.name),"wb") as f:
                    f.write((file).getbuffer())
            files_lenght = len(os.listdir(files_folder))

            # Run the PDF Inspector
            report = PyPDFInspector()
            report.run_pdf_inspector_from_folder(
                file_path=files_folder,
                persistent_folder=vectordb_folder,
                )
            st.success(f"Arquivos Carregados: {files_lenght}. Código do trabalho: {key}")
    
            return key

if __name__ == "__main__":
    upload_files(type=['pdf', 'docx', 'doc', 'txt'])