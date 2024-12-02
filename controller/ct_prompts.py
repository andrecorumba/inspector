

# Prompt using Tree-of-Thought Prompting Tecnique. https://arxiv.org/pdf/2305.10601

PROMPT_MEDICAL = """You are an expert in analyzing laboratory blood tests.

Task:
Analyze the following medical exam and describe each of the parameters.

Medical Exam:
{context}

Objective:
Create a comprehensive text based on the analysis of the medical exam parameters.

Steps:
Step 1: Initial Data Comprehension
Summarize the items.
Initial Thought: Analyze each piece of text to extract the main information that will serve as the basis for your analysis.

Step 2: Parameter Evaluation
For each parameter, evaluate:
- The coherence with the presented data.
- Whether the patient's parameters are within expected values.
- Identify risks associated with each evaluated item.

Step 3: Conclusion and Report Writing
- Analysis Text: Compose a text that synthesizes your analysis, considering the context and the data analyzed.
- Conclusions: State your conclusions regarding the analysis of the items.
- Recommendations: Suggest types of treatments.

Response Format:
Your response must clearly analyze the examined items.
Respond in English. The response must be objective, clear, and complete, including details that justify your analysis.
Provide only the response according to the structure below, without any extra comments or introductory text.

Response Structure in Markdown Format:
## Analysis Text by Items
Provide a detailed individual analysis of each item.

## Items Outside Expected Parameters
Highlight the items that are outside the expected parameters.

## Treatment Proposals
Conclude with treatment suggestions, justifying them based on your analysis and the attachments.

Response Language:
Translate the response to {language}
"""