# prompts.py

::: controller.prompts

## Portugues prompts

```
from langchain.prompts import PromptTemplate

prompt_template = """
A partir de trechos de documentos constantes do contexto a seguir e responda a pergunta do usuário.
Contexto: {context}
Pergunta: {question}
A resposta deve ser clara, direta e formal em português, seguindo o conteúdo do contexto.
Você deverá responder apenas se houver uma resposta no contexto acima, caso contrário escreva apenas: 
"Não consegui encontrar a resposta nos documentos fornecidos."
"""
PORTUGUESE_BASIC_PROMPT = PromptTemplate.from_template(prompt_template)
```