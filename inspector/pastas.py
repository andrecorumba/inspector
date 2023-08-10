import os

# Importando módulos internos
import chave

def cria_pastas(pasta_usuario, chave):
    '''
    Cria as pastas necessárias para o funcionamento da aplicação.
    Se as pastas já existirem, retorna o caminho.

    Parâmetros:
        pasta_usuario (str): Caminho da pasta principal do usuário
        chave (str): Chave aleatória do trabalho do usuário.

    Retornos:
        pasta_do_trabalho (str): Caminho da pasta do trabalho.
        pasta_vectordb (str): Caminho da pasta do vectordb.
        pasta_database (str): Caminho da pasta do banco de dados.
        pasta_temporaria (str): Caminho da pasta temporária.
        pasta_aquivos (str): Caminho da pasta original.
    '''

    # Cria a pasta principal do usuário caso não exista.
    if not os.path.exists(pasta_usuario):
        os.makedirs(pasta_usuario)

    # Traça o caminho e cria a para a pasta do trabalho do usuário
    pasta_do_trabalho = os.path.join(pasta_usuario, chave)
    if not os.path.exists(pasta_do_trabalho):
        os.makedirs(pasta_do_trabalho)

    # Caminho para as subpastas de cada trabalho chave_ide
    pasta_vectordb = os.path.join(pasta_do_trabalho, "vectordb")
    pasta_database = os.path.join(pasta_do_trabalho, "database")
    pasta_temporaria = os.path.join(pasta_do_trabalho, "temporary")
    pasta_aquivos= os.path.join(pasta_do_trabalho, "files")

    # Cria as subpastas caso não existam
    for subfolder_path in [pasta_vectordb, pasta_database, pasta_temporaria, pasta_aquivos]:
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
    

def pega_pasta(usuario, chave_do_trabalho, tipo_de_pasta):
    if tipo_de_pasta == 'pasta_do_usuario':
        pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    '..', 
                                    'data', 
                                    usuario)

    elif tipo_de_pasta == 'pasta_do_trabalho':
        pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    '..', 
                                    'data', 
                                    usuario, 
                                    chave_do_trabalho)

    else:
        pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    '..', 
                                    'data', 
                                    usuario, 
                                    chave_do_trabalho,
                                    tipo_de_pasta)
    
    return pasta



if __name__ == '__main__':
    cria_pastas('data/usuario', 
                'd_12345678')