import os

def create_folders(user_folder, work_key):
    """
    Create folders for a new user.

    Parameters:
    folder_user (str): Path to the user folder.
    """

    # Cria a folder principal do usuário caso não exista.
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)

    # Traça o caminho e cria a para a folder do trabalho do usuário
    work_folder = os.path.join(user_folder, work_key)
    if not os.path.exists(work_folder):
        os.makedirs(work_folder)

    # Caminho para as subfolders de cada trabalho chave_ide
    vectordb_folder = os.path.join(work_folder, "vectordb")
    download_folder = os.path.join(work_folder, "download")
    responses_folder = os.path.join(work_folder, "responses")
    upload_folder= os.path.join(work_folder, "upload")

    # Cria as subfolders caso não existam
    for subfolder_path in [vectordb_folder, download_folder, responses_folder, upload_folder]:
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
    # Any type of folder
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