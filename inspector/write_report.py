import pandas as pd
import requests

from dotenv import load_dotenv, find_dotenv

import os

import json

class Report():
    '''Class to write report from the results of the analysis.'''

    def __init__(self, id=None, path=None):
        self.id = id
        self.path = path
        self.json_content = None
        self.eaud_api_key = None

        if id:
            self.load_from_request_page(id)
        elif path:
            self.load_from_json_file(path)

    def load_from_request_page(self, id):
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
            self.path = path
            try:
                with open(path, "r", encoding="utf-8") as file:
                    self.json_content = json.load(file)
                # print(self.json_content)
                print(self.json_content["data"][0]["descricaoSumaria"])
            except FileNotFoundError:
                print(f"File not found: {path}")
            except Exception as e:
                print(f"An error occurred while reading the JSON file: {e}")

def main():
    report = Report(path="/Users/andreluiz/Downloads/inspector-examples/matriz-de-achados/response_1694810668864.json")
    # report = Report(id=1197908)

if __name__ == "__main__":
    main()