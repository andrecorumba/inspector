import string
import random

def cria_chave(tipo_de_trabalho):
    ''' 
    Função que cria uma chave aleatória para identificar o caso de uso do app.

    Parâmetros:
        tipo_de_trabalho (str): Tipo de trabalho que o usuário está fazendo. Use sem espaços.

    Retornos:
        Chave (str): Chave aleatória de 08 caracteres.
    '''

    # Gera uma chave aleatória com 8 caracteres
    tamanho_chave = 8
    caracteres_permitidos = string.ascii_letters + string.digits
    aleatorio = ''.join(random.choice(caracteres_permitidos) for _ in range(tamanho_chave))
    
    # Concatena o tipo_de_trabalho com a chave aleatória
    chave = tipo_de_trabalho + '_' + aleatorio
    
    return chave

if __name__ == '__main__':
    print(cria_chave('documentos'))