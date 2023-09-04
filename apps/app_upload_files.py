import streamlit as st
import sys
import os

from inspector import folders, password, chave

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

def upload_files(type) -> str:
    """
    Function to upload files to the user folder.

    Parameters:
    type (list): List of file types.

    Return:
    work_key (str): Work key.
    """

    st.file_uploader('Selecione os arquivos para análise', 
                     type=type,
                     accept_multiple_files=True,
                     key='uploaded_file_list')
    
    if st.session_state['uploaded_file_list'] is not None:
        if st.button('Processar Arquivos'):
            user_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                        '..', 
                                        'data', 
                                        password.user)
            
            work_key = chave.cria_chave('documentos')

            folders.create_folders(user_folder, work_key)

            files_folder = folders.get_folder(password.user, 
                                                  work_key, 
                                                  'files')
                        
            for file in st.session_state['uploaded_file_list']:
                with open(os.path.join(files_folder, file.name),"wb") as f:
                    f.write((file).getbuffer())
            
            files_lenght = len(os.listdir(files_folder))

            st.success(f"Sucesso! Quantidade de Arquivos Carregados: {files_lenght}")
            st.markdown(f"### Código deste trabalho: *{work_key}*")
    
            return work_key

if __name__ == "__main__":
    upload_files(type=['pdf', 'docx', 'doc', 'txt'])