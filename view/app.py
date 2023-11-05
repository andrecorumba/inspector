# Import External Modules
import streamlit as st
from streamlit_option_menu import option_menu

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import internal modules
from view import (
    app_upload_files, 
    app_py_pdf_inspector
    )

# Main function for the Inspector App
def main(user='user'):
    """ Main function for the Inspector App. """
    with st.sidebar:
        st.write("Usuário da sessão:", user)
        option = option_menu("Inspector v.0.1.1",
                            options=["Página Inicial", 
                                     "Carregar Documentos",
                                     "Interagir com Documentos",
                                     ],                    
                            # Icons from https://icons.getbootstrap.com/
                            icons=["house", 
                                   "archive",
                                   "chat-dots",
                                   ]
                                   )   
    if option == "Página Inicial":
        st.title("Página Inicial")
        st.markdown("""O **Inspector** é uma POC de aplicação web, escrita em Python, 
                    que analisa e interage com vários tipos de documentos.
                    """)   
    elif option == "Carregar Documentos":   
        app_upload_files.upload_files(type=['pdf'], user=user)
    elif option == "Interagir com Documentos":   
        app_py_pdf_inspector.app(user)
    
if __name__ == '__main__':
    main()