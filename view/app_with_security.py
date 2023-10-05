# Import External Modules
import streamlit as st
from streamlit_option_menu import option_menu

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import internal modules
from controller import folders
from view import (
    password,
    app,
)


def main():
    """ Main function for the Inspector App with security. """
    if password.check_password():
        app.main(user=password.user)

        
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

if __name__ == '__main__':
    main()