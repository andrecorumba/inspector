import streamlit as st
import random
from upload import upload_file
from call_endpoints import call_endpoint

def app():
    """
    Medical Examination Analysis Page.

    This app allows users to upload files and analyze medical examinations 
    by sending the file to a backend API.
    """
    st.title("Medical Examination Analysis")
    st.markdown("""
                Welcome to the Medical Examination Analysis module.
                Please upload a document for analysis.
                """
                )

    select_document = "Supported documents: PDF, DOCX, XLSX, CSV, MD, TXT"
    st.markdown(f"**{select_document}**")

    uploaded_file = st.file_uploader(
        label="Upload your document here",  
        type=['pdf', 'docx', 'xlsx', 'csv', 'md', 'txt'], 
        key='uploaded_file', 
        accept_multiple_files=False
        )

    if uploaded_file:
        button_run = st.button('Run Analysis')
        if button_run:
            type_of_analysis = 'medical'
            task_id = str(random.randint(0, 9999))  # Generate a random task ID
            
            if 'user' not in st.session_state:
                st.session_state['user'] = 'default_user'
            
            try:
                response_upload = upload_file(uploaded_file, task_id, type_of_analysis, st.session_state['user'])
                if response_upload:
                    parameters = {
                        "user": st.session_state['user'],
                        "task_id": task_id,
                        "type_of_analysis": type_of_analysis,
                    }
                    st.write("Parameters sent for analysis:", parameters)
                    
                    api_route = '/medical'
                    task_response = call_endpoint(api_route, parameters)
                    if task_response.get('error'):
                        st.error(f"Error: {task_response['error']}")
                    else:
                        st.success("Successfully sent for analysis! Check the status and response in the side menu.")
                else:
                    st.error("Failed to upload the file. Please try again.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")