import streamlit as st
import os

from inspector import folders, risks, password
from apps import app_upload_files

def app():
    # user_work_list = []
    # for item in os.listdir(folders.get_folder(user=password.user,
    #                                             work_key='todos',
    #                                             type_of_folder='user_folder')):
    #     if not item.startswith('.'):
    #         user_work_list.append(item)

    # with st.sidebar:
    #     option_work = st.selectbox(label="Lista de Trabalhos",
    #                                 options=user_work_list)
    #     st.write('Você Selecionou:', option_work)
    #     st.session_state['work_folder'] = folders.get_folder(user=password.user,
    #                                                                 work_key=option_work,
    #                                                                 type_of_folder='work_folder')

    work_key = app_upload_files.upload_files(type=['pdf'])
    if work_key is not None:
        # st.button('Identificar Riscos', key='button_risk_mode')     
        
        # if st.session_state['button_risk_mode']:           
        database_folder = folders.get_folder(password.user, work_key, 'database') 
        with st.spinner("Identificando Riscos modo REFINE .... 💫"):                  
            response_risk_refined_mode, cb, files_loaded = risks.risks_identifier(password.user, work_key)      
        with open(os.path.join(database_folder, 'risks_type_refine.txt'), 'w') as f:
            f.write(f"RELATÓRIO DE IDENTIFICAÇÃO DE RISCOS\n\n{files_loaded}\n\n{cb}\n\n{response_risk_refined_mode}\n\n")
        st.success("Riscos identificados com sucesso! 🎉")
        st.write(cb)
        st.write(response_risk_refined_mode)


if __name__ == "__main__":
    app()