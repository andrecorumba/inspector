# Importando módulos externos
import streamlit as st
from streamlit_option_menu import option_menu
import os

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
                                options=["Home", 
                                        "Carregar Documentos", 
                                        "Analisar Documentos",
                                        "Identificar Riscos"],
                                
                                # Ícones de https://icons.getbootstrap.com/
                                icons=['house', 
                                       "filetype-pdf",
                                       "search",
                                       "activity"])            
        # Página Home
        if option == "Home":
            st.title("Home")
            st.markdown("""O **Inspector** é uma aplicação web, escrita em Python, 
                        que analisa vários tipos de documentos.
                        """)   

        # Página Carregar Documentos
        elif option == "Carregar Documentos":
            st.title("Carregar Documentos")
            st.write("Página para analisar documentos.")
            
            #documentos.analisador_arquivos_pdf(password.usuario)

            chave_do_trabalho = upload_arquivos(type=['pdf'])

            if chave_do_trabalho:
                pdf_inspector.pdf_load_split_vector(password.usuario, chave_do_trabalho)
                pdf_inspector.generate_first_questions(password.usuario, chave_do_trabalho)


        # Página Analisar Documentos
        elif option == "Analisar Documentos":   

            try:

                # Cria lista de trabalhos do usuário
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
                pdf_inspector.user_questions(password.usuario, option_trabalho)
                                                       
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
                pdf_inspector.risk_identification(password.usuario, option_trabalho)
            
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
    
    # Verifica se os arquivos foram upados
    if uploaded_file_list is not None:
        if st.button('Carregar Arquivos'):

            # Constrói o caminho absoluto para a pasta "data" a partir do diretório atual
            pasta_usuario = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    '..', 
                                    'data', 
                                    password.usuario)
            
            # Cria chave de acesso com base no tipo de trabalho (documentos)
            chave_do_trabalho = chave.cria_chave('documentos')

            # Criar pasta e subpastas do trabalho do usuário
            pastas.cria_pastas(pasta_usuario, chave_do_trabalho)

            # Pega pasta de arquivos
            pasta_de_arquivos = pastas.pega_pasta(password.usuario, 
                                                  chave_do_trabalho, 
                                                  'files')
                        
            # Salva todos os arquivos upados
            for file in uploaded_file_list:
                with open(os.path.join(pasta_de_arquivos, file.name),"wb") as f:
                    f.write((file).getbuffer())
            
            quantidade_arquivos = len(os.listdir(pasta_de_arquivos))

            st.success(f"Sucesso! Quantidade de Arquivos Carregados: {quantidade_arquivos}")
            st.markdown(f"### Código deste trabalho: *{chave_do_trabalho}*")
    
            return chave_do_trabalho

if __name__ == '__main__':
    main()