# Importando módulos externos
import streamlit as st
from streamlit_option_menu import option_menu

import os

import json

# Importando módulos internos
import password
import chave
import pastas
import pdf_inspector


def main():
    '''Função principal do app.'''

    if password.check_password():
    
        # Menu Lateral
        with st.sidebar:

            st.write("Usuário da sessão:", password.usuario)

            option = option_menu("Inspector v.0.1.0",
                                options=["Página Inicial", 
                                        "Carregar Documentos", 
                                        "Analisar Documentos",
                                        "Identificar Riscos"],
                                
                                # Ícones de https://icons.getbootstrap.com/
                                icons=['house', 
                                       "filetype-pdf",
                                       "search",
                                       "activity"])            
        # Página Home
        if option == "Página Inicial":
            st.title("Página Inicial")
            st.markdown("""O **Inspector** é uma aplicação web, escrita em Python, 
                        que analisa vários tipos de documentos.
                        """)   

        elif option == "Carregar Documentos":
            st.title("Carregar Documentos")
            st.write("Página para analisar documentos.")

            chave_do_trabalho = upload_arquivos(type=['pdf'])

            if chave_do_trabalho:
                pdf_inspector.pdf_load_split_vector(password.usuario, chave_do_trabalho)
                pdf_inspector.generate_first_questions(password.usuario, chave_do_trabalho)

        elif option == "Analisar Documentos":   

            try:
                lista_de_trabalhos_usuario = []
                for item in os.listdir(pastas.pega_pasta(usuario=password.usuario,
                                                        chave_do_trabalho='todos',
                                                        tipo_de_pasta='pasta_do_usuario')):
                    if not item.startswith('.'):
                        lista_de_trabalhos_usuario.append(item)
            
                with st.sidebar:
                    option_trabalho = st.selectbox(label="Lista de Trabalhos",
                                          options=lista_de_trabalhos_usuario)
                    st.write('Você Selecionou:', option_trabalho)
                   
                    st.session_state['pasta_do_trabalho'] = pastas.pega_pasta(usuario=password.usuario,
                                                                              chave_do_trabalho=option_trabalho,
                                                                              tipo_de_pasta='pasta_do_trabalho')
                    
                    st.radio('Selecione', options=['Mostrar Histório',
                                                   'Responder Perguntas Prontas',
                                                   'Fazer Minhas Perguntas'], 
                                                   key='radio_show_questions')

       
                if st.session_state['radio_show_questions'] == 'Mostrar Histório':
                    show_all(password.usuario, option_trabalho)
                
                elif st.session_state['radio_show_questions'] == 'Responder Perguntas Prontas':
                    st.multiselect('Selecione as perguntas', 
                                   options=get_questions(password.usuario, option_trabalho),
                                   key='multiselect_questions')
                    
                    if st.button('Responder'):
                        for query in st.session_state['multiselect_questions']:
                            pdf_inspector.user_questions(password.usuario, option_trabalho, query)

                elif st.session_state['radio_show_questions'] == 'Fazer Minhas Perguntas':
                    if query:=st.text_input("Digite sua pergunta:"):                          
                        pdf_inspector.user_questions(password.usuario, option_trabalho, query)
                                                       
            except FileNotFoundError:
                st.warning('Não há trabalhos para analisar. Por favor, carregue documentos.')
                return
            
        elif option == "Identificar Riscos":   
            try:

                lista_de_trabalhos_usuario = []
                for item in os.listdir(pastas.pega_pasta(usuario=password.usuario,
                                                        chave_do_trabalho='todos',
                                                        tipo_de_pasta='pasta_do_usuario')):
                    if not item.startswith('.'):
                        lista_de_trabalhos_usuario.append(item)
            
                with st.sidebar:
                    option_trabalho = st.selectbox(label="Lista de Trabalhos",
                                          options=lista_de_trabalhos_usuario)
                    st.write('Você Selecionou:', option_trabalho)
                   
                    st.session_state['pasta_do_trabalho'] = pastas.pega_pasta(usuario=password.usuario,
                                                                              chave_do_trabalho=option_trabalho,
                                                                              tipo_de_pasta='pasta_do_trabalho')
                    

                # Analisar Documentos                 
                if agency:=st.text_input("Digite o nome ou a sigla da unidade auditada:"):                   
                    pdf_inspector.risk_identifier(password.usuario, option_trabalho, agency)
            
            except FileNotFoundError:
                st.warning('Não há trabalhos para analisar. Por favor, carregue documentos.')
                return


def upload_arquivos(type):
    """
    Função para fazer o upload dos arquivos para o servidor.

    Parâmetros:
    pasta_usuario (str): Caminho absoluto para a pasta do usuário.
    chave_do_trabalho (str): Chave de acesso ao trabalho.

    Retorno:
    pasta_do_trabalho (str): Caminho absoluto para a pasta do trabalho.
    """

    uploaded_file_list = st.file_uploader('Selecione os arquivos PDF para análise', 
                                          type=type,
                                          accept_multiple_files=True)
    
    if uploaded_file_list is not None:
        if st.button('Carregar Arquivos'):
            pasta_usuario = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    '..', 
                                    'data', 
                                    password.usuario)
            
            chave_do_trabalho = chave.cria_chave('documentos')

            pastas.cria_pastas(pasta_usuario, chave_do_trabalho)

            pasta_de_arquivos = pastas.pega_pasta(password.usuario, 
                                                  chave_do_trabalho, 
                                                  'files')
                        
            for file in uploaded_file_list:
                with open(os.path.join(pasta_de_arquivos, file.name),"wb") as f:
                    f.write((file).getbuffer())
            
            quantidade_arquivos = len(os.listdir(pasta_de_arquivos))

            st.success(f"Sucesso! Quantidade de Arquivos Carregados: {quantidade_arquivos}")
            st.markdown(f"### Código deste trabalho: *{chave_do_trabalho}*")
    
            return chave_do_trabalho

def show_all(usuario, chave_do_trabalho):
    """ Função para mostrar todos as perguntas e respostas do trabalho.
    
    Parâmetros:
    usuario (str): Nome do usuário.
    chave_do_trabalho (str): Chave de acesso ao trabalho.

    Retorno:
    None
    """

    database_folder = pastas.pega_pasta(usuario, 
                                        chave_do_trabalho, 
                                        'database')
    
    with open(os.path.join(database_folder, 'qa.txt'), 'r') as f:
        qa = f.readlines()
        for line in qa:
            st.write(line)

def get_questions(user, work_key):
    """ Função para selecionar as perguntas da pré-análise.
    
    Parâmetros:
    user (str): Nome do usuário.
    work_key (str): Chave de acesso ao trabalho.
    """

    database_folder = pastas.pega_pasta(user, 
                                        work_key, 
                                        'database')
    
    with open(os.path.join(database_folder, 'qa.json'), 'r') as f:
        qa = json.load(f)
        questions = qa[0]['result'].split('\n')

    return questions


if __name__ == '__main__':
    main()