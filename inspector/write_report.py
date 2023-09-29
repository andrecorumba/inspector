import pandas as pd
import requests

from dotenv import load_dotenv, find_dotenv

import os

import json

import openai

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from inspector.prompts import WRITE_REPORT_PROMPT


class Report():
    '''Class to write report from the results of the analysis.'''

    def __init__(self, id=None, path=None):
        self.id = id
        self.path = path
        self.json_content = None
        self.eaud_api_key = None
        self.context = []

        if id:
            self.load_from_request_page(id)
        elif path:
            self.load_from_json_file(path)

    def load_from_request_page(self, id):
        '''Function to load the JSON content from the EAUD API.
        This is a solution to e-aud system from CGU. https://eaud.cgu.gov.br/'''

        _ = load_dotenv(find_dotenv())
        self.eaud_api_key = os.environ['EAUD_API_KEY']

        if not self.eaud_api_key:
            raise ValueError("EAUD_API_KEY environment variable is not set.")

        url = f"https://eaud.cgu.gov.br/api/auth/execucao/achado-auditoria/{id}/itens"
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "chave-api": self.eaud_api_key
        }

        response = requests.request("GET", url, headers=headers)

        if response.status_code == 200:
            self.json_content = response.json()
            print(self.json_content)
        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")

    def load_from_json_file(self, path):
        '''Function to load the JSON content from a file.
        The JSON file must be in the same format as the e-aud system.'''

        self.path = path
        try:
            with open(path, "r", encoding="utf-8") as file:
                self.json_content = dict(json.load(file))
                
                # Loop to get the context from the JSON file.
                for i in range(len(self.json_content["data"])):
                    description = "Descrição Sumária: " + str(self.json_content["data"][i]["descricaoSumaria"])
                    analysis = ''

                    for j in range(len(self.json_content["data"][i]["analisesDoItemAchadoAuditoria"])):                        
                        test = "Teste de Auditoria: " + str(self.json_content["data"][i]["analisesDoItemAchadoAuditoria"][j]["itemAnaliseAuditoria"]["teste"])
                        scope = "Escopo da Auditoria: " + str(self.json_content["data"][i]["analisesDoItemAchadoAuditoria"][j]["itemAnaliseAuditoria"]["escopos"])
                        evidences = "Escopo da Auditoria: " + str(self.json_content["data"][i]["analisesDoItemAchadoAuditoria"][j]["itemAnaliseAuditoria"]["evidencias"])
                        analysis += test + scope + evidences
                    self.context.append("Descrição Sumária: " + description + "\n" "Análise: " + analysis + "\n\n")             
        except FileNotFoundError:
            print(f"File not found: {path}")
        except Exception as e:
            print(f"An error occurred while reading the JSON file: {e}")
    
    def get_api_key(self, text_input_openai_api_key = 'openai'):
        '''Function to get OpenAI API key from the environment variable or from the text input.'''

        if text_input_openai_api_key == 'openai':
            _ = load_dotenv(find_dotenv())
            api_key = os.environ['OPENAI_API_KEY']
        else:
            api_key = text_input_openai_api_key
        return api_key
    
    def llm_write_report(self, context):
        '''Function to write the report using the LLM model.'''

        openai.api_key = self.get_api_key()
        llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k", 
                        openai_api_key=openai.api_key,
                        temperature=0.6,
                        max_tokens=8000)
        llm_chain = LLMChain(prompt=WRITE_REPORT_PROMPT, llm=llm)
        response = llm_chain.run(context)
        return {"achado" : response}


def main():
    '''Main function to test the class.'''
    
    report = Report(path="/Users/andreluiz/Downloads/inspector-examples/matriz-de-achados/response_1694810668864.json")
    # report = Report(id=1197908)

    list_of_responses = []
    for i, context in enumerate(report.context):
        list_of_responses.append(report.llm_write_report(context))

    print(list_of_responses)

if __name__ == "__main__":
    main()