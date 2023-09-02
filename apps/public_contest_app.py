import streamlit as st

def app():
    st.markdown("# Concurso Público")
    st.markdown("""Faça upload de um Edital de Concurso Público e obtenha as respostas para as perguntas mais frequentes.""")

    st.file_uploader('Faça upload do Edital em PDF para análise',
                    type=['pdf'],
                    accept_multiple_files=False,
                    key='uploaded_file_public_contest')

if __name__ == "__main__":
    app()