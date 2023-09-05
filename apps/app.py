# Import External Modules
import streamlit as st
from streamlit_option_menu import option_menu

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import internal modules
from apps import app_risks


def main():
    """ Main function for the Inspector App. """

    with st.sidebar:
        st.write("Usuário da sessão:", 'user')

        option = option_menu("Inspector v.0.1.0",
                            options=["Página Inicial", 
                                    "Identificar Riscos"],
                            
                            # Icons from https://icons.getbootstrap.com/
                            icons=['house', 
                                    "search"])   
    if option == "Página Inicial":
        st.title("Página Inicial")
        st.markdown("""O **Inspector** é uma aplicação web, escrita em Python, 
                    que analisa vários tipos de documentos.
                    """)   
    elif option == "Identificar Riscos":   
        app_risks.app('user')
    
    
if __name__ == '__main__':
    main()