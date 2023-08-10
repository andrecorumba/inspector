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
        
        # Menu lateral
        with st.sidebar:

            st.write("Usuário da sessão:", password.usuario)

            option = option_menu("Inspector v.0.1.0",
                                options=["Home", 
                                        "Carregar Documentos", 
                                        "Analisar Documentos"],
                                
                                # Ícones de https://icons.getbootstrap.com/
                                icons=['house', 
                                       "filetype-pdf",
                                       "search"])            
        # Página Home
        if st.session_state['option_menu'] == "Home":
            st.title("Home")
            st.markdown("""O **Inspector** é uma aplicação web, escrita em Python, 
                        que analisa vários tipos de documentos.
                        """)   

        # Página Carregar Documentos
        elif st.session_state['option_menu'] == "Carregar Documentos":
            st.title("Carregar Documentos")
            st.write("Página para analisar documentos.")
            
            chave_do_trabalho = upload_arquivos(type=['pdf'])
            if chave_do_trabalho:
                pdf_inspector.pdf_load_split_vector(password.usuario, chave_do_trabalho)
                pdf_inspector.generate_first_questions(password.usuario, chave_do_trabalho)


        # Página Analisar Documentos
        elif st.session_state['option_menu'] == "Analisar Documentos":   
            try:
                lista_de_trabalhos_usuario = []
                pasta_do_usuario = pastas.pega_pasta(usuario=password.usuario,
                                                     chave_do_trabalho='todos',
                                                     tipo_de_pasta='pasta_do_usuario')

                for item in os.listdir(pasta_do_usuario):
                    if not item.startswith('.'):
                        lista_de_trabalhos_usuario.append(item)

                with st.sidebar:
                    st.selectbox(label="Lista de Trabalhos",
                                          options=lista_de_trabalhos_usuario,
                                          key='option_work')
                    
                    st.write('Você Selecionou:', st.session_state['option_work'])
                   
                    pasta_do_trabalho = pastas.pega_pasta(usuario=password.usuario,
                                                          chave_do_trabalho=st.session_state['option_work'],
                                                          tipo_de_pasta='pasta_do_trabalho')
                    

                # Analisar Documentos                                   
                pdf_inspector.user_questions(password.usuario, option_trabalho)
                    

                                            
            except FileNotFoundError:
                st.warning('Não há trabalhos para analisar. Por favor, carregue documentos.')
                return


def upload_arquivos(type):
    """
    Função para fazer o upload dos arquivos para o servidor.

    Parâmetros:
    type (str): Tipo de arquivo a ser upado.

    Retorno:
    chave_do_trabalho (str): Chave do trabalho.
    """

    uploaded_file_list = st.file_uploader('Selecione os arquivos PDF para análise', 
                                          type=type,
                                          accept_multiple_files=True)
    
    # Verifica se os arquivos foram upados
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

if __name__ == '__main__':
    main()