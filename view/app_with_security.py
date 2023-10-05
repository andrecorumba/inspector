# Import External Modules
import streamlit as st
from streamlit_option_menu import option_menu

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import json

# Import internal modules
from inspector import password, folders, pdf_inspector

from apps import public_contest_app, app_risks, app_upload_files, app_write_report


def main():
    """ Main function for the Inspector App. """

    if password.check_password():

        with st.sidebar:
            st.write("Usuário da sessão:", password.user)

            option = option_menu("Inspector v.0.1.0",
                                options=["Página Inicial", 
                                        "Carregar Documentos", 
                                        "Analisar Documentos",
                                        ],
                                
                                # Icons from https://icons.getbootstrap.com/
                                icons=['house', 
                                       "filetype-pdf",
                                       "search",
                                       ])   
            
        if option == "Página Inicial":
            st.title("Página Inicial")
            st.markdown("""O **Inspector** é uma aplicação web, escrita em Python, 
                        que analisa vários tipos de documentos.
                        """)   

        elif option == "Carregar Documentos":
            st.title("Carregar Documentos")
            st.write("Página para analisar documentos.")

            work_key = app_upload_files.upload_files(type=['pdf'], 
                                                     type_of_work='documentos',
                                                     user=password.user)
            if work_key:
                pdf_inspector.pdf_load_split_vector(password.user, work_key)

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
                    
                    st.radio('Selecione', options=[# 'Mostrar Histório',
                                                   'Fazer Minhas Perguntas',
                                                   'Gerar Perguntas Prontas',], 
                                                   key='radio_show_questions')
                    
                if st.session_state['radio_show_questions'] == 'Fazer Minhas Perguntas':
                    if query:=st.text_input("Digite sua pergunta:"):                          
                        pdf_inspector.user_questions(password.user, option_work, query)

                # if st.session_state['radio_show_questions'] == 'Mostrar Histório':
                #     show_all(password.user, option_work)
                
                elif st.session_state['radio_show_questions'] == 'Gerar Perguntas Prontas':
                    get_questions(password.user, option_work)
                    
                                                       
            except FileNotFoundError:
                st.warning('Não há trabalhos para analisar. Por favor, carregue documentos.')
                return


def show_all(user, work_key):
    """
    Function to show all questions and answers.

    Parameters:
    user (str): User name.
    work_key (str): Work key.

    Return:
    None
    """

    response_folder = folders.get_folder(user, 
                                         work_key, 
                                         'response')
    
    # Verifica se existe o arquivo qa.txt
    if not os.path.exists(os.path.join(response_folder, 'qa.txt')):
        st.warning('Não há perguntas e respostas para mostrar. Faça perguntas.')
    
        with open(os.path.join(response_folder, 'qa.txt'), 'r') as f:
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

    response_folder = folders.get_folder(user, 
                                        work_key, 
                                        'response')
    
    questions = pdf_inspector.generate_first_questions(password.user, work_key)  
    
    # with open(os.path.join(response_folder, 'qa.json'), 'r') as f:
    #     qa = json.load(f)
    #     questions = qa[0]['result'].split('\n')

    return questions

if __name__ == '__main__':
    main()