import string
import random
#import uuid

def create_key(type_of_work):
    ''' 
    Função que cria uma chave aleatória para identificar o caso de uso do app.

    Parâmetros:
        tipo_de_trabalho (str): Tipo de trabalho que o usuário está fazendo. Use sem espaços.

    Retornos:
        Chave (str): Chave aleatória de 08 caracteres.
    '''

    # Create a random combination of letters and numbers
    len_key = 6
    # letters = string.ascii_letters + string.digits
    # combination = ''.join(random.choice(letters) for _ in range(len_key))
    combination = ''.join(random.choice(string.digits) for _ in range(len_key))
    
    # Concatenate the type of work with the combination
    key = type_of_work + '_' + combination
    # key = str(uuid.uuid4())

    return key

if __name__ == '__main__':
    print(create_key('documentos'))