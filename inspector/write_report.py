import pandas as pd
import requests

from dotenv import load_dotenv, find_dotenv

import os

class Report():
    '''Class to write report from the results of the analysis.'''

    def __init__(self, path):
        self.path = path

    def request_page(self, id):
        _ = load_dotenv(find_dotenv())
        eaud_api_key = os.environ['EAUD_API_KEY']


        url = F"https://eaud.cgu.gov.br/api/auth/execucao/achado-auditoria/{id}/itens"

        payload = ""
        headers = {
            #"cookie": "BIGipServer~INTERNA~pool_https_sdp_k8s2_traefik=rd1o00000000000000000000ffff0a7d1f5do30002; SESSION=MmQ3ZDdlOWUtZjA1OS00MTE5LTk4MDEtMzBlZmMwMjQ5OWY1",
            "Content-Type": "application/json;charset=UTF-8",
            "chave-api": eaud_api_key
        }

        response = requests.request("GET", url, data=payload, headers=headers)

        print(response.text)

def main():
    report = Report("/Users/andreluiz/Downloads/inspector-examples/matriz-de-achados/response_1694810668864.json")
    report.request_page(id=1197908)

if __name__ == "__main__":
    main()