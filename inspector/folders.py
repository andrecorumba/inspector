import os

# Importando módulos internos
import chave

def create_folders(folder_user, work_key):
    """
    Create folders for a new user.

    Parameters:
    folder_user (str): Path to the user folder.
    """

    # Cria a folder principal do usuário caso não exista.
    if not os.path.exists(folder_user):
        os.makedirs(folder_user)

    # Traça o caminho e cria a para a folder do trabalho do usuário
    folder_do_trabalho = os.path.join(folder_user, work_key)
    if not os.path.exists(folder_do_trabalho):
        os.makedirs(folder_do_trabalho)

    # Caminho para as subfolders de cada trabalho chave_ide
    folder_vectordb = os.path.join(folder_do_trabalho, "vectordb")
    folder_database = os.path.join(folder_do_trabalho, "database")
    folder_temporaria = os.path.join(folder_do_trabalho, "temporary")
    folder_aquivos= os.path.join(folder_do_trabalho, "files")

    # Cria as subfolders caso não existam
    for subfolder_path in [folder_vectordb, folder_database, folder_temporaria, folder_aquivos]:
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
    

def get_folder(user, work_key, type_of_folder):
    if type_of_folder == 'user_folder':
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    '..', 
                                    'data', 
                                    user)

    elif type_of_folder == 'work_folder':
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    '..', 
                                    'data', 
                                    user, 
                                    work_key)

    else:
        folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    '..', 
                                    'data', 
                                    user, 
                                    work_key,
                                    type_of_folder)
    
    return folder



if __name__ == '__main__':
    create_folders('data/user', 
                'd_12345678')