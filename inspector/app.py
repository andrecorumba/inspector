# Importando módulos externos
import streamlit as st
from streamlit_option_menu import option_menu
import os

# Importando módulos internos
import documentos
import password
import analisar
import processar_llm

from password import usuario

def main():
    '''
    Função principal do app.
    '''

    if password.check_password():
    
    
        # Menu Lateral
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
        if option == "Home":
            st.title("Home")
            st.markdown("""O **Inspector** é uma aplicação web, escrita em Python, 
                        que analisa vários tipos de documentos.
                        """)   

        # Página Carregar Documentos
        elif option == "Carregar Documentos":
            st.title("Carregar Documentos")
            st.write("Página para analisar documentos.")
            
            documentos.analisador_arquivos_pdf(password.usuario)

        # Página Analisar Documentos
        elif option == "Analisar Documentos":   

            try:
                lista_de_trabalhos_usuario = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                                                     '..', 
                                                                     'data', 
                                                                     password.usuario))
            
                with st.sidebar:
                    option_trabalho = st.selectbox(label="Lista de Trabalhos",
                                          options=lista_de_trabalhos_usuario)
                    st.write('Você Selecionou:', option_trabalho)
                    pasta_do_trabalho = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                                     '..', 
                                                     'data', 
                                                     password.usuario, 
                                                     option_trabalho)
                    
                # Analisar Documentos                                   
                analisar.pergunta_do_usuario(password.usuario, option_trabalho)
                                            
            except FileNotFoundError:
                st.warning('Não há trabalhos para analisar. Por favor, carregue documentos.')
                return
        
if __name__ == '__main__':
    main()