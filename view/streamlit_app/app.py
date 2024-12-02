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

st.set_page_config(
    page_title="Inspector",
    page_icon="material/medication_liquid",
)

def main(user='user'):
    """
    Main application entry point.

    Args:
        user (str): Default user name for the application.
    """
    with st.sidebar:
        st.text(f"Version: {load_version()}")
        option = option_menu(
            menu_title="Inspector",
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
            label='Input your user',
            value=user,
            max_chars=50,
            key='user',
        )

        st.radio(
            label="Choose the service used in your .env file",
            options=["azure", "openai"],
            index=1,
            disabled=True,
            key="service_option",
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
    """Load the application version from a file."""
    version_file_path = 'view/streamlit_app/version.txt'
    if os.path.exists(version_file_path):
        with open(version_file_path, "r") as f:
            return f.read().strip()
    else:
        return "Version not found"


if __name__ == '__main__':
    main()