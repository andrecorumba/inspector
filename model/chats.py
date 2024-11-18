from openai import AzureOpenAI
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from model.config_schema import SaveRedisPydantic
import json

class AzureChatInsight:
    """
    A class for interacting with Azure OpenAI services to invoke chat-based insights using specified prompts and contexts.

    Attributes:
        client_chat (AzureOpenAI): The AzureOpenAI client initialized with environment variables for API keys and configurations.
    """

    def __init__(self) -> None:
        """
        Initializes the AzureChatInsight instance by setting up the AzureOpenAI client using environment variables.
        """
        self.client_chat = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment=os.getenv("AZURE_DEPLOYMENT"),
        )

    def invoke(self, prompt: str, context: str, persona: str)->str:
        """
        Invokes the Azure OpenAI chat completion API with a specified prompt, context, and persona.

        Args:
            prompt (str): The main user input to the chat model.
            context (str): Additional context to be included in the conversation.
            persona (str): The system persona or instructions for the model's behavior.

        Returns:
            str: A JSON representation of the API's response, including the generated content and usage statistics.
        """
        self.messages = [
            {
                "role": "system",
                "content": persona,
            },
            {
                "role": "user",
                "content": prompt + str(context),
            },
        ]

        self.completion = self.client_chat.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
        )
        self.response = self.completion.choices[0].message.content
        self.response_json = self.completion.to_json()
        self.usage = self.completion.usage.to_json()
        self.context = context

        return self.response_json
