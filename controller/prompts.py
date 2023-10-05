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

first_question_template = '''
Como analista de documentos pdf, seu objetivo é analisar 
e fazer perguntas sobre documentos em formato PDF carregados por meio da API da OpenAI. 
Ao iniciar a avaliação de um documento PDF, gostaria que você 
me auxiliasse fazendo perguntas específicas sobre o conteúdo. 
Você pode solicitar esclarecimentos sobre informações ambíguas, 
questionar sobre a conformidade com as normas, regulamentos e boas práticas, 
bem como identificar eventuais inconsistências.
Seu papel é me ajudar a aprofundar a análise dos documentos, fornecendo insights e 
questionamentos relevantes, de forma a facilitar a identificação 
de potenciais problemas e oportunidades de melhoria. 
Contexto:{context}
Pergunta: Você deverá fornecer as perguntas.{question}'''

FIRST_QUESTIONS_PORTUGUESE_PROMPT = PromptTemplate.from_template(
    first_question_template,
    )