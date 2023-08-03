# Importando módulos externos
import streamlit as st
import os

# Importando módulos internos
import chave
import pastas
import processar_llm
import analisar

def analisador_arquivos_pdf(usuario):
    """
    Função que analisa arquivos PDF.

    Parâmetros:
    usuario (str): Nome do usuário.
    """
    
    # Constrói o caminho absoluto para a pasta "data" a partir do diretório atual
    pasta_usuario = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', usuario)
    
    # Cria chave de acesso com base no tipo de trabalho (documentos)
    chave_do_trabalho = chave.cria_chave('documentos')

    # Fazer upload de arquivos
    pasta_do_trabalho = upload_arquivos(pasta_usuario, chave_do_trabalho)

    # Processar LLM na pasta dos arquivos
    if pasta_do_trabalho:
        processar_llm.processar_llm(pasta_do_trabalho)
        analisar.pre_analise(usuario, chave_do_trabalho)


def upload_arquivos(pasta_usuario, chave_do_trabalho):
    """
    Função para fazer o upload dos arquivos para o servidor.

    Parâmetros:
    pasta_usuario (str): Caminho absoluto para a pasta do usuário.
    chave_do_trabalho (str): Chave de acesso ao trabalho.

    Retorno:
    pasta_do_trabalho (str): Caminho absoluto para a pasta do trabalho.
    """

    uploaded_file_list = st.file_uploader('Selecione os arquivos PDF para análise', 
                                          type=["pdf"],
                                          accept_multiple_files=True)
    
    # Verifica se os arquivos foram upados
    if uploaded_file_list is not None:
        if st.button('Carregar Arquivos'):

            # Criar pasta e subpastas do trabalho do usuário
            (pasta_do_trabalho, 
            pasta_vectordb, 
            pasta_database, 
            pasta_temporaria,
            pasta_aquivos) = pastas.cria_pastas(pasta_usuario, chave_do_trabalho)
                        
            # Salva todos os arquivos upados
            for file in uploaded_file_list:
                with open(os.path.join(pasta_aquivos, file.name),"wb") as f:
                    f.write((file).getbuffer())
            
            quantidade_arquivos = len(os.listdir(pasta_aquivos))

            st.success(f"Sucesso! Quantidade de Arquivos Carregados: {quantidade_arquivos}")
            st.markdown(f"### Código deste trabalho: *{chave_do_trabalho}*")

            return pasta_do_trabalho