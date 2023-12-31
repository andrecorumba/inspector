# Inspector

O **Inspector** é uma Prova de Conceito (POC), contendo aplicação web e scripts, escritos em Python, que analisam vários tipos de documentos. Ela se  utiliza de modelos de linguagem GPT-3.5 e GPT-4 da OpenAI para fornecer respostas com base em perguntas feitas pelo usuário.

## Funcionalidades

- Carregar Documentos: Permite ao usuário fazer o upload de arquivos PDF para análise.
- Analisar Documentos: Utiliza o LangChain e o modelo GPT-3.5-turbo para analisar documentos PDF e responder perguntas.

## Documentação

A documentação do código encontra-se em:

https://andrecorumba.github.io/inspector/

## Exemplo da Aplicação

Uma PoC para identificar riscos está disponível em:

http://inspector.streamlit.app/

## Estrutura de Diretórios

O projeto possui uma estrutura de diretórios que inclui as seguintes pastas:
- **model:** Nesta pasta, estão arquivos Python relacionados à modelagem ou manipulação de dados.
- **view:** A pasta "view" contém arquivos Python relacionados à interface do usuário.
- **controller:** Nesta pasta, encontram-se arquivos Python relacionados à lógica de controle da aplicação.
- **tests:** A pasta "tests" contém scripts de teste para a aplicação.
- **docs:** A pasta "docs" contém documentação do projeto.

## Arquivos de Configuração

- **.vscode:** Esta pasta contém configurações e arquivos relacionados ao Visual Studio Code.
- **.gitignore:** O arquivo ".gitignore" especifica quais arquivos e diretórios devem ser ignorados pelo Git durante o versionamento do código-fonte.
- **LICENSE:** O arquivo "LICENSE" contém informações sobre a licença do projeto.
- **README.md:** O arquivo "README.md" contém essas instruções.
- **mkdocs.yml:** Arquivo de configuração usado para gerar documentação utilizando a ferramenta MkDocs.
- **poetry.lock** e **pyproject.toml:** Esses arquivos estão relacionados à gestão de dependências e configuração do ambiente Python usando a ferramenta Poetry.

## Pré-requisitos

Certifique-se de ter as seguintes bibliotecas instaladas:

- streamlit
- streamlit_option_menu
- openai
- dotenv
- langchain

Você pode instalar as bibliotecas usando o gerenciador de pacotes `pip`. Por exemplo:

```
pip install streamlit
pip install streamlit-option-menu
pip install langchain
pip install openai
pip install python-dotenv
pip install pypdf
pip install tiktoken
pip install chromadb
pip install watchdog
```

## Como Executar o Projeto

1. Clone o repositório:

```
git clone https://github.com/andrecorumba/inspector.git
```

2. Acesse o diretório do projeto:

```
cd inspector
```

3. Crie um arquivo `.env` na raiz do projeto com sua chave da API da OpenAI:

```
OPENAI_API_KEY=sua-chave-da-api-da-openai
```

4. Crie uma pasta oculta na raiz do projeto `.streamlit/secrets.toml` com o conteúdo dos usuários e senhas.
```
[passwords]
# Follow the rule: username = "password"
alice_foo = "streamlit123"
bob_bar = "mycrazypw"
```

5. Execute o aplicativo com Streamlit:

```
streamlit run view/app_with_security.py
```

ou para app sem uso de senha digite:
```
streamlit run view/app.py
```

6. O aplicativo será executado em seu navegador padrão. Você pode acessá-lo em `http://localhost:8501`.

## Como Usar o App

1. Ao iniciar o aplicativo, será solicitado que você insira seu nome de usuário e senha. Digite suas credenciais corretas para acessar as funcionalidades do aplicativo.

2. Na barra lateral esquerda, você encontrará as diferentes opções disponíveis: "Home", "Carregar Documentos", etc.

3. Selecione a opção desejada e siga as instruções para utilizar cada funcionalidade do aplicativo.

## Observações

- Certifique-se de que sua chave da API da OpenAI esteja correta e configurada corretamente no arquivo `.env`.

## Autores

- andrecorumba

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um "issue" ou enviar um "pull request" com melhorias ou correções.

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para obter mais detalhes.

## Descrição das funções principais de cada arquivo:

### `app.py`

O arquivo `app.py` contém a função principal do projeto chamada `main()`. Essa função é responsável por criar a interface do usuário do aplicativo utilizando o framework Streamlit. O app tem um menu lateral que permite ao usuário escolher entre diferentes opções, como carregar documentos, analisar documentos PDF, elaborar matriz de planejamento, analisar conversas do WhatsApp e escrever relatórios.

A função `main()` é executada quando o arquivo `app.py` é executado diretamente. Ela verifica se a senha do usuário é correta usando a função `password.check_password()`. Em seguida, dependendo da opção selecionada pelo usuário no menu lateral, ele é redirecionado para a página correspondente.

### `py_pdf_inspector.py`

O arquivo `py_pdf_inspector.py` contém a classe `PyPDFInspector`, que é responsável por analisar arquivos PDF.

### `password.py`

O arquivo `password.py` contém a função `check_password()`, que é responsável por verificar se a senha inserida pelo usuário está correta. Ela utiliza o framework Streamlit para exibir campos de entrada para o nome de usuário e senha. Se a senha estiver correta, a função retorna `True`, caso contrário, retorna `False`.

### `folders.py`

O arquivo `folders.py` contém a função `create_folders(user_folder, work_key)`, que é responsável por criar as pastas necessárias para o funcionamento do aplicativo. Ela recebe o caminho da pasta principal do usuário e uma chave aleatória como entrada e cria as pastas relacionadas ao trabalho do usuário.

### `work_key.py`

O arquivo `work_key.py` contém a função `create_key(type_of_work)`, que é responsável por criar uma chave aleatória para identificar o caso de uso do app.

Outras funcionalidades ainda em construção.

## Bibliotecas usadas:

- `streamlit`: Um framework de criação de aplicativos web interativos com Python.
- `streamlit_option_menu`: Uma extensão do Streamlit que permite criar menus de seleção personalizados.
- `openai`: Uma biblioteca de Python para interagir com a API da OpenAI e usar modelos de linguagem como o GPT-3.5-turbo.
- `dotenv`: Uma biblioteca para carregar variáveis de ambiente a partir de um arquivo `.env`.
- `langchain`: Uma biblioteca para processamento de linguagem natural e uso do modelo GPT-3.5-turbo da OpenAI.
- `os`: Uma biblioteca que permite interagir com o sistema operacional, como criar pastas e manipular arquivos.
- `string`: Uma biblioteca para manipular strings em Python, utilizada para gerar chaves aleatórias.
- `random`: Uma biblioteca para geração de números aleatórios em Python.

## Para Depurar o Projeto no VSCode:

O arquivo launch.json é uma parte essencial do ambiente de desenvolvimento para projetos Python no Visual Studio Code. Ele é usado para configurar e definir as configurações de depuração (debug) para um projeto específico. No exemplo abaixo, explicarei as diferentes propriedades do arquivo launch.json e o que elas significam
Altere o arquivo `launch.json` constante da pasta `.vscode` para o conteúdo a seguir:

```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Streamlit",
            "type": "python",
            "request": "launch",
            "program": ".venv/bin/streamlit",
            "console": "integratedTerminal",
            "justMyCode": true,
            "args": ["run", "inspector/app.py"]
        }
    ]
}
```