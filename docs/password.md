# Password

::: inspector.password

## Descrição do Código
Este código em Python utiliza a biblioteca Streamlit para criar uma interface de usuário interativa que solicita ao usuário um nome de usuário e uma senha. O objetivo é verificar se o usuário forneceu a senha correta associada ao nome de usuário. O código utiliza o conceito de "session_state" para armazenar temporariamente informações entre diferentes interações do usuário com a aplicação.

O código original disponível em: https://docs.streamlit.io/knowledge-base/deploy/authentication-without-sso

Aqui está uma descrição detalhada do código:

1. O código importa a biblioteca Streamlit e define uma função chamada `check_password()` que realiza a verificação da senha:

2. Dentro da função `check_password()`, há uma função interna chamada `password_entered()`. Esta função é usada para verificar se a senha digitada pelo usuário está correta.

3. Na função `password_entered()`, a senha fornecida pelo usuário é comparada com a senha correta armazenada na variável `st.secrets["passwords"]`, que é uma configuração secreta definida na aplicação do Streamlit (mais sobre isso posteriormente). Se a senha estiver correta, a variável de estado `st.session_state["password_correct"]` é definida como `True`, indicando que a senha está correta. Em caso contrário, é definida como `False`.

4. A função principal `check_password()` começa verificando se a variável de estado `password_correct` não está presente em `st.session_state`. Isso é usado para verificar se é a primeira vez que o usuário interage com o aplicativo.

5. Se `password_correct` ainda não estiver definida, o aplicativo exibe campos de entrada de texto para o usuário digitar seu nome de usuário e senha. Esses campos são vinculados à função `password_entered()` por meio do parâmetro `on_change`, o que significa que a função será chamada automaticamente sempre que o conteúdo dos campos de entrada for alterado.

6. Se `password_correct` não estiver definida e o usuário preencher o nome de usuário e a senha, a função `password_entered()` será chamada para verificar se a senha está correta. Se estiver correta, a variável de estado `password_correct` será definida como `True`, caso contrário, será definida como `False`.

7. Se `password_correct` estiver definida, mas seu valor for `False`, isso significa que o usuário já tentou entrar com a senha, mas a senha estava incorreta. Nesse caso, o aplicativo mostra novamente os campos de entrada de texto para que o usuário possa tentar novamente. Além disso, uma mensagem de erro é exibida usando `st.error()` para informar ao usuário que o nome de usuário não é conhecido ou a senha está incorreta.

8. Se a variável `password_correct` estiver definida e seu valor for `True`, isso significa que o usuário inseriu a senha correta. Nesse caso, a função retorna `True`, indicando que a senha está correta.

Para funcionar corretamente, o código presume que haja uma configuração secreta definida no Streamlit com o nome `"passwords"` que mapeia nomes de usuário para suas respectivas senhas corretas. Além disso, é necessário que a aplicação do Streamlit tenha habilitado a funcionalidade de sessão para armazenar as variáveis de estado entre as interações do usuário.

Esse código é uma implementação básica de autenticação simples, sem qualquer recurso de armazenamento seguro de senhas ou gerenciamento de usuários. Ele é adequado apenas para fins de demonstração e pode não ser seguro o suficiente para uso em um ambiente de produção. Em aplicações reais, é essencial implementar uma autenticação mais robusta e segura.

## Sobre a função interna.

A função `check_password` contém outra função chamada `password_entered`. A estrutura de ter uma função dentro de outra é conhecida como função aninhada ou função interna. Essa abordagem é usada para encapsular e organizar o código de maneira mais eficiente, especialmente quando a função interna é relevante apenas para a função externa e não precisa ser acessada de outros lugares.

Aqui estão algumas razões pelas quais você pode encontrar funções aninhadas em um código:

1. **Escopo limitado**: A função `password_entered` é útil apenas para a função `check_password`. Colocá-la dentro da função externa garante que ela só possa ser usada nesse contexto específico.

2. **Compartilhamento de variáveis**: A função interna tem acesso às variáveis da função externa. Isso é útil para evitar a necessidade de passar essas variáveis como argumentos para a função interna.

3. **Encapsulamento**: A função interna não precisa ser acessada por outras partes do código. Ao colocá-la dentro da função externa, você está indicando claramente que ela é relevante apenas para a lógica específica da função externa.

4. **Organização**: Funções aninhadas podem ajudar a dividir uma tarefa complexa em etapas menores. Isso pode melhorar a legibilidade e manutenibilidade do código.

5. **Menos poluição de namespace**: Ao usar funções internas, você evita poluir o espaço de nomes global com funções que só são relevantes em um contexto específico.

No caso específico desse código, a função `password_entered` é uma parte essencial da verificação do nome de usuário e senha inseridos. Ela verifica se o nome de usuário e a senha correspondem ao que está armazenado nos segredos do Streamlit e define uma variável de estado `password_correct` de acordo. Essa função aninhada é usada para modularizar a lógica de verificação do nome de usuário e senha, tornando o código mais organizado e legível.