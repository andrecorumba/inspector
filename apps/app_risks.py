import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from inspector import folders, risks
from apps import app_upload_files

def app(user):
    """ Main function for the Risks App."""
    st.text_input("OpenAI API Key", key="openai_api_key", type="password")
    st.markdown("[Obtenha uma OpenAI API key](https://platform.openai.com/account/api-keys)")
    
    if st.session_state['openai_api_key'] != "":
        # get OpenAI API Key
        risks.get_api_key(st.session_state['openai_api_key'])
    
        # get work key
        work_key = app_upload_files.upload_files(type=['pdf'], type_of_work='riscos', user=user)
        
        if work_key is not None:
            response_folder = folders.get_folder(user, work_key, 'responses') 
            
            # call risk identifier
            with st.spinner("Identificando Riscos .... 💫"):                  
                (response_risk_refined_mode, 
                    cb, 
                    zip_file) = risks.risk_identifier_individual_file(user, 
                                                                    work_key, 
                                                                    st.session_state['openai_api_key'])
            st.success("Riscos identificados com sucesso! 🎉")

            # dowload response files
            with open(os.path.join(response_folder, zip_file), 'rb') as f:
                st.download_button(label="Baixar Relatório de Riscos",
                                    data=f,
                                    file_name=zip_file,
                                    mime='application/zip')

if __name__ == "__main__":
    app()