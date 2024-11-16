from openai import AzureOpenAI
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from model.config_schema import SaveRedisPydantic
import json


class AzureChatInsight():
    def __init__(self) -> None:
        self.client_chat = AzureOpenAI(
            api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
            api_version = os.getenv("OPENAI_API_VERSION"),
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment = os.getenv("AZURE_DEPLOYMENT"),
        )

    def invoke(self, prompt: str, context: str, persona: str):
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