Aqui está o conteúdo para o arquivo README.md do projeto "Auditor-Copilot":

# Inspector

O **Inspector** é uma aplicação web, escrita em Python, que analisa vários tipos de documentos de forma mais eficiente. Ela se  utiliza o poder do modelo de linguagem GPT-3.5-turbo da OpenAI para fornecer respostas formais e precisas com base em perguntas feitas pelo usuário.

## Funcionalidades

- Carregar Documentos: Permite ao usuário fazer o upload de arquivos PDF para análise.
- Analisar Documentos: Utiliza o LangChain e o modelo GPT-3.5-turbo para analisar documentos PDF e responder perguntas do auditor.
- Elaborar Matriz de Planejamento: Opção para elaborar uma matriz de planejamento de forma interativa.
- Analisar Conversas Whatsapp: Permite analisar conversas do WhatsApp.
- Escrever Relatórios: Página para escrever relatórios.

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
pip install streamlit_option_menu
pip install openai
pip install dotenv
pip install langchain
```

## Como Executar o Projeto

1. Clone o repositório:

```
git clone https://github.com/seu-usuario/Auditor-Copilot.git
```

2. Acesse o diretório do projeto:

```
cd Auditor-Copilot
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

5. Execute o aplicativo Streamlit:

```
streamlit run app.py
```

6. O aplicativo será executado em seu navegador padrão. Você pode acessá-lo em `http://localhost:8501`.

## Como Usar o App

1. Ao iniciar o aplicativo, será solicitado que você insira seu nome de usuário e senha. Digite suas credenciais corretas para acessar as funcionalidades do aplicativo.

2. Na barra lateral esquerda, você encontrará as diferentes opções disponíveis: "Home", "Carregar Documentos", "Analisar Documentos", "Elaborar Matriz de Planejamento", "Analisar Conversas Whatsapp" e "Escrever Relatórios".

3. Selecione a opção desejada e siga as instruções para utilizar cada funcionalidade do aplicativo.

## Observações

- Certifique-se de que sua chave da API da OpenAI esteja correta e configurada corretamente no arquivo `.env`.

## Autores

- Seu Nome
- Seu Colega

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um "issue" ou enviar um "pull request" com melhorias ou correções.

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para obter mais detalhes.

## Descrição das funções principais de cada arquivo:

### `app.py`

O arquivo `app.py` contém a função principal do projeto chamada `main()`. Essa função é responsável por criar a interface do usuário do aplicativo utilizando o framework Streamlit. O app tem um menu lateral que permite ao usuário escolher entre diferentes opções, como carregar documentos, analisar documentos PDF, elaborar matriz de planejamento, analisar conversas do WhatsApp e escrever relatórios.

A função `main()` é executada quando o arquivo `app.py` é executado diretamente. Ela verifica se a senha do usuário é correta usando a função `password.check_password()`. Em seguida, dependendo da opção selecionada pelo usuário no menu lateral, ele é redirecionado para a página correspondente.

### `documentos.py`

O arquivo `documentos.py` contém a função `analisador_arquivos_pdf(usuario)`, que é responsável por analisar arquivos PDF. A função recebe o nome do usuário como entrada e permite que o usuário faça upload de arquivos PDF para análise.

### `password.py`

O arquivo `password.py` contém a função `check_password()`, que é responsável por verificar se a senha inserida pelo usuário está correta. Ela utiliza o framework Streamlit para exibir campos de entrada para o nome de usuário e senha. Se a senha estiver correta, a função retorna `True`, caso contrário, retorna `False`.

### `pastas.py`

O arquivo `pastas.py` contém a função `cria_pastas(pasta_usuario, chave)`, que é responsável por criar as pastas necessárias para o funcionamento do aplicativo. Ela recebe o caminho da pasta principal do usuário e uma chave aleatória como entrada e cria as pastas relacionadas ao trabalho do usuário.

### `processar_llm.py`

O arquivo `processar_llm.py` contém duas funções principais:

1. `processar_llm(pasta_do_trabalho)`: Esta função é responsável por processar o LangChain, que envolve carregar os documentos PDF da pasta de trabalho, criar embeddings (representações vetoriais) para esses documentos usando o modelo GPT-3.5-turbo-16k da OpenAI e armazenar esses embeddings no diretório persistente para uso posterior.

2. `carrega_documento_pdf(pasta_arquivos)`: Esta função é responsável por carregar os documentos PDF da pasta de arquivos usando o LangChain. Os documentos são divididos em pedaços menores para facilitar o processamento.

## Bibliotecas usadas:

- `streamlit`: Um framework de criação de aplicativos web interativos com Python.
- `streamlit_option_menu`: Uma extensão do Streamlit que permite criar menus de seleção personalizados.
- `openai`: Uma biblioteca de Python para interagir com a API da OpenAI e usar modelos de linguagem como o GPT-3.5-turbo.
- `dotenv`: Uma biblioteca para carregar variáveis de ambiente a partir de um arquivo `.env`.
- `langchain`: Uma biblioteca para processamento de linguagem natural e uso do modelo GPT-3.5-turbo da OpenAI.
- `os`: Uma biblioteca que permite interagir com o sistema operacional, como criar pastas e manipular arquivos.
- `string`: Uma biblioteca para manipular strings em Python, utilizada para gerar chaves aleatórias.
- `random`: Uma biblioteca para geração de números aleatórios em Python.