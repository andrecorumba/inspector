# Import External Modules
import streamlit as st
from streamlit_option_menu import option_menu
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from view.streamlit_app import (
    page_home,
    page_medical,
    page_responses,
    page_status, 
)


def main(user='user'):
    """
    Main application entry point.

    Args:
        user (str): Default user name for the application.
    """
    with st.sidebar:
        option = option_menu(
            menu_title=load_version(),
            options=[
                'Home',
                'Medical Tests',
                'Status',
                'Responses',
            ],
            # Icons from https://icons.getbootstrap.com/
            icons=[
                'house',
                'eyeglasses',
                'easel2',
                'robot',
            ],
        )
        st.text_input(
            label='User',
            value=user,
            max_chars=50,
            key='user',
        )
    
    # Sidebar navigation logic
    if option == 'Home':
        page_home.app()
    elif option == 'Medical Tests':
        page_medical.app()
    elif option == 'Status':
        page_status.app()
    elif option == 'Responses':
        page_responses.app()


def load_version():
    """
    Load the application version from a file.

    Returns:
        str: The version of the application, or a default value if the file is not found.
    """
    version_file_path = 'view/streamlit_app/version.txt'
    if os.path.exists(version_file_path):
        with open(version_file_path, "r") as f:
            return f.read().strip()
    else:
        return "Version not found"


if __name__ == '__main__':
    main()