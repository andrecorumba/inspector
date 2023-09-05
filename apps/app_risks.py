import streamlit as st
import os

from inspector import folders, risks, password
from apps import app_upload_files

def app(user):
    # user_work_list = []
    # for item in os.listdir(folders.get_folder(user=user,
    #                                             work_key='todos',
    #                                             type_of_folder='user_folder')):
    #     if not item.startswith('.'):
    #         user_work_list.append(item)

    # with st.sidebar:
    #     option_work = st.selectbox(label="Lista de Trabalhos",
    #                                 options=user_work_list)
    #     st.write('Você Selecionou:', option_work)
    #     st.session_state['work_folder'] = folders.get_folder(user=user,
    #                                                                 work_key=option_work,
    #                                                                 type_of_folder='work_folder')

    work_key = app_upload_files.upload_files(type=['pdf'], type_of_work='riscos', user=user)
    if work_key is not None:
        # st.button('Identificar Riscos', key='button_risk_mode')     
        
        # if st.session_state['button_risk_mode']:           
        response_folder = folders.get_folder(user, work_key, 'responses') 
        with st.spinner("Identificando Riscos .... 💫"):                  
            #response_risk_refined_mode, cb, files_loaded = risks.risks_identifier(user, work_key)      
            response_risk_refined_mode, cb, zip_file = risks.risk_identifier_individual_file(user, work_key)

        # response_file_name = f'{work_key}.txt'
        
        # save response files
        # with open(os.path.join(database_folder, response_file_name), 'w') as f:
        #     f.write(f"RELATÓRIO DE IDENTIFICAÇÃO DE RISCOS\n\n{files_loaded}\n\n{cb}\n\n{response_risk_refined_mode}\n\n")
        
        # print response files
        st.success("Riscos identificados com sucesso! 🎉")
        # st.write(cb)
        # st.write(response_risk_refined_mode)

        # dowload response files
        with open(os.path.join(response_folder, zip_file), 'rb') as f:
            st.download_button(label="Baixar Relatório de Riscos",
                                data=f,
                                file_name=zip_file,
                                mime='application/zip')



if __name__ == "__main__":
    app()