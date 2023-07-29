# Importando módulos externos
import streamlit as st
from streamlit_option_menu import option_menu

# Importando módulos internos
import documentos
import password
import analisar


def main():
    '''
    Função principal do app.
    '''

    if password.check_password():
    
        # Menu Lateral
        with st.sidebar:
            option = option_menu("Versão Web v.0.1.0",
                                options=["Home", 
                                        "Carregar Documentos", 
                                        "Analisar Documentos",
                                        "Elaborar Matriz de Planejamento",
                                        "Analisar Conversas Whatsapp",
                                        "Escrever Relatórios"],
                                
                                # Ícones de https://icons.getbootstrap.com/
                                icons=['house', 
                                       "filetype-pdf",
                                       "search",
                                       "table",
                                       "whatsapp",
                                       "pencil"])
            
        # Página Home
        if option == "Home":
            st.title("Home")
            st.write("Página inicial do app.")   

        # Página Carregar Documentos
        elif option == "Carregar Documentos":
            st.title("Carregar Documentos")
            st.write("Página para analisar documentos.")
            
            documentos.analisador_arquivos_pdf('andrelmr')

        # Página Analisar Documentos
        elif option == "Analisar Documentos":
            st.title("Analisar Documentos")
            st.write("Página para analisar documentos.")

            analisar.analisar_documentos_pdf('andrelmr')

        # Página Elaborar Matriz de Planejamento
        elif option == "Elaborar Matriz de Planejamento":
            st.title("Elaborar Matriz de Planejamento")
            st.write("Página para elaborar matriz de planejamento.")

        # Página Analisar Conversas Whatsapp
        elif option == "Analisar Conversas Whatsapp":
            st.title("Analisar Conversas Whatsapp")
            st.write("Página para analisar conversas do whatsapp.")
        
        # Página Escrever Relatórios
        elif option == "Escrever Relatórios":
            st.title("Escrever Relatórios")
            st.write("Página para escrever relatórios.")


if __name__ == '__main__':
    main()