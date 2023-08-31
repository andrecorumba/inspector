# Import External Modules
import streamlit as st
from streamlit_option_menu import option_menu

import os

import json

# Import internal modules
import password
import chave
import folders
import pdf_inspector
import risks


def main():
    """ Main function for the Inspector App. """

    if password.check_password():

        with st.sidebar:
            st.write("Usuário da sessão:", password.user)

            option = option_menu("Inspector v.0.1.0",
                                options=["Página Inicial", 
                                        "Carregar Documentos", 
                                        "Analisar Documentos",
                                        "Identificar Riscos"],
                                
                                # Icons from https://icons.getbootstrap.com/
                                icons=['house', 
                                       "filetype-pdf",
                                       "search",
                                       "activity"])            
            
        if option == "Página Inicial":
            st.title("Página Inicial")
            st.markdown("""O **Inspector** é uma aplicação web, escrita em Python, 
                        que analisa vários tipos de documentos.
                        """)   

        elif option == "Carregar Documentos":
            st.title("Carregar Documentos")
            st.write("Página para analisar documentos.")

            work_key = upload_arquivos(type=['pdf'])
            if work_key:
                pdf_inspector.pdf_load_split_vector(password.user, work_key)
                pdf_inspector.generate_first_questions(password.user, work_key)

        elif option == "Analisar Documentos":   
            try:
                user_work_list = []
                for item in os.listdir(folders.get_folder(user=password.user,
                                                        work_key='todos',
                                                        type_of_folder='user_folder')):
                    if not item.startswith('.'):
                        user_work_list.append(item)
            
                with st.sidebar:
                    option_work = st.selectbox(label="Lista de Trabalhos",
                                               options=user_work_list)
                    st.write('Você Selecionou:', option_work)

                    st.session_state['work_folder'] = folders.get_folder(user=password.user,
                                                                              work_key=option_work,
                                                                              type_of_folder='work_folder')
                    
                    st.radio('Selecione', options=['Mostrar Histório',
                                                   'Responder Perguntas Prontas',
                                                   'Fazer Minhas Perguntas'], 
                                                   key='radio_show_questions')

                if st.session_state['radio_show_questions'] == 'Mostrar Histório':
                    show_all(password.user, option_work)
                
                elif st.session_state['radio_show_questions'] == 'Responder Perguntas Prontas':
                    st.multiselect('Selecione as perguntas', 
                                   options=get_questions(password.user, option_work),
                                   key='multiselect_questions')
                    
                    if st.button('Responder'):
                        for query in st.session_state['multiselect_questions']:
                            pdf_inspector.user_questions(password.user, option_work, query)

                elif st.session_state['radio_show_questions'] == 'Fazer Minhas Perguntas':
                    if query:=st.text_input("Digite sua pergunta:"):                          
                        pdf_inspector.user_questions(password.user, option_work, query)
                                                       
            except FileNotFoundError:
                st.warning('Não há trabalhos para analisar. Por favor, carregue documentos.')
                return
            
        elif option == "Identificar Riscos":   
            try:
                user_work_list = []
                for item in os.listdir(folders.get_folder(user=password.user,
                                                         work_key='todos',
                                                         type_of_folder='user_folder')):
                    if not item.startswith('.'):
                        user_work_list.append(item)
            
                with st.sidebar:
                    option_work = st.selectbox(label="Lista de Trabalhos",
                                               options=user_work_list)
                    st.write('Você Selecionou:', option_work)
                   
                    st.session_state['work_folder'] = folders.get_folder(user=password.user,
                                                                              work_key=option_work,
                                                                              type_of_folder='work_folder')
                    st.radio('Tipo de Análise', options=['Refine Mode',
                                                   'Recursive Mode'], 
                                                   key='radio_risk_mode')
                    st.button('Identificar Riscos', key='button_risk_mode')

                # Risk Identifier      
                if st.session_state['button_risk_mode']:           
                    if st.session_state['radio_risk_mode'] == 'Refine Mode':
                        database_folder = folders.get_folder(password.user, option_work, 'database') 
                        with st.spinner("Identificando Riscos modo REFINE .... 💫"):                  
                            # Risk Identifier from refined template
                            response_risk_refined_mode = risks.risks_identifier(password.user, option_work)
                            with open(os.path.join(database_folder, 'risks_type_refine.txt'), 'w') as f:
                                f.write(response_risk_refined_mode)
                            st.success("Riscos no modo Refine identificados com sucesso! 🎉")
                    
                    elif st.session_state['radio_risk_mode'] == 'Recursive Mode':
                        with st.spinner("Identificando Riscos modo RECURSIVE .... 💫"):
                            # Risk Identifier from recursive sqlite
                            response_risk_recursive_mode = pdf_inspector.risk_identifier(password.user, option_work)
                            with open(os.path.join(database_folder, 'risks_type_recursive_sqlite.txt'), 'w') as f:
                                f.write(response_risk_recursive_mode)
                            st.success("Riscos no modo recursive identificados com sucesso! 🎉")

 
                        # st.write(f"Riscos Identificados para a Unidade: {agency}")     
                        # st.write(f"{response_risk}")
            
            except Exception as e:
                st.warning('Problemas ao carregar os arquivos. Por favor, carregue documentos.')
                return


def upload_arquivos(type):
    """
    Function to upload files to the user folder.

    Parameters:
    type (list): List of file types.

    Return:
    work_key (str): Work key.
    """

    st.file_uploader('Selecione os arquivos PDF para análise', 
                     type=type,
                     accept_multiple_files=True,
                     key='uploaded_file_list')
    
    if st.session_state['uploaded_file_list'] is not None:
        if st.button('Carregar Arquivos'):
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

def show_all(user, work_key):
    """
    Function to show all questions and answers.

    Parameters:
    user (str): User name.
    work_key (str): Work key.

    Return:
    None
    """

    database_folder = folders.get_folder(user, 
                                         work_key, 
                                         'database')
    
    with open(os.path.join(database_folder, 'qa.txt'), 'r') as f:
        qa = f.readlines()
        for line in qa:
            st.write(line)

def get_questions(user, work_key):
    """
    Funtion to get all questions.

    Parameters:
    user (str): User name.
    work_key (str): Work key.

    Return:
    questions (list): List of questions.
    """

    database_folder = folders.get_folder(user, 
                                        work_key, 
                                        'database')
    
    with open(os.path.join(database_folder, 'qa.json'), 'r') as f:
        qa = json.load(f)
        questions = qa[0]['result'].split('\n')

    return questions

if __name__ == '__main__':
    main()