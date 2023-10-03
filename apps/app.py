# Import External Modules
import streamlit as st
from streamlit_option_menu import option_menu

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import internal modules
from apps import (
    app_risks, 
    app_write_report, 
    app_upload_files, 
    app_py_pdf_inspector
    )


def main():
    """ Main function for the Inspector App. """
    with st.sidebar:
        st.write("Usuário da sessão:", 'user')
        option = option_menu("Inspector v.0.1.1",
                            options=["Página Inicial", 
                                     "Carregar Documentos",
                                     "Interagir com Documentos",
                                     "Identificar Riscos",
                                     "Escrever Relatório"],                    
                            # Icons from https://icons.getbootstrap.com/
                            icons=["house", 
                                   "archive",
                                   "chat-dots",
                                   "search",
                                   "pencil-fill"]
                                   )   
    if option == "Página Inicial":
        st.title("Página Inicial")
        st.markdown("""O **Inspector** é uma POC de aplicação web, escrita em Python, 
                    que analisa e interage com vários tipos de documentos.
                    """)   
    elif option == "Carregar Documentos":   
        app_upload_files.upload_files(type=['pdf'])
    elif option == "Interagir com Documentos":   
        app_py_pdf_inspector.app('user')
    elif option == "Identificar Riscos":   
        app_risks.app('user')
    elif option == "Escrever Relatório":   
        app_write_report.app('user')

    
if __name__ == '__main__':
    main()