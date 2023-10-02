# Import External Modules
import streamlit as st
from streamlit_option_menu import option_menu

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import internal modules
from apps import app_risks, app_write_report


def main():
    """ Main function for the Inspector App. """
    with st.sidebar:
        st.write("Usuário da sessão:", 'user')
        option = option_menu("Inspector v.0.1.0",
                            options=["Página Inicial", 
                                    "Identificar Riscos",
                                    "Escrever Relatório",
                                    "Converse com o Relatório"],                    
                            # Icons from https://icons.getbootstrap.com/
                            icons=['house', 
                                    "search",
                                    "pencil-fill",
                                    "chat-right-text-fill"])   
    if option == "Página Inicial":
        st.title("Página Inicial")
        st.markdown("""O **Inspector** é uma POC de aplicação web, escrita em Python, 
                    que analisa e interage com vários tipos de documentos.
                    """)   
    elif option == "Identificar Riscos":   
        app_risks.app('user')
    elif option == "Escrever Relatório":   
        app_write_report.app('user')
    elif option == "Converse com o Relatório":   
        app_write_report.app('user')
    
if __name__ == '__main__':
    main()