import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from inspector import write_report

def app(user: str = "user"):
    """ Main function for the Write Report App.
    
    Parameters:
    user (str): User name.
    
    Return:
    None
    """
    
    uploaded = st.file_uploader('Selecione os arquivos para análise', 
                type=["json"],
                accept_multiple_files=False,
                key='upload_write_report')
    
    if uploaded:
        if st.button("Analisar"):
            with st.spinner("Escrevendo Relatório de Auditoria. 💫"):
                temporary_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temporary')

                with open(os.path.join(temporary_folder, uploaded.name),"wb") as f:
                    f.write(uploaded.getbuffer())


                json_path = os.path.join(temporary_folder, uploaded.name)
                
                report = write_report.Report(path=json_path)
                list_of_responses = []
                for context in report.context:
                    list_of_responses.append(report.llm_write_report(context))          
                st.success("Relatórios Processados com Sucesso! 🎉")
                st.write(list_of_responses)

if __name__ == "__main__":
    app()