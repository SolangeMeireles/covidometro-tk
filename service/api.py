from os.path import dirname, realpath, isfile
from json import load
from decouple import config

import requests

class ApiService():

    def __init__(self):
        pass
    

    def load_data(self):
        data = self.read_json('/db.json')
        return data


    def search(state, city):
        API_TOKEN = config('TOKEN_BRASIL_API', default="")

        url_api = f"https://api.brasil.io/v1/dataset/covid19/caso_full/data/?city={city}&state={state}&page_size=1"

        headers = {
            "Authorization": f"Token {API_TOKEN}",
            "User-Agent": "python-urlib/brasilio-client-0.1.0"
        }

        results = []  # Zera o array

        try:
            print('Aguarde enquanto buscamos os dados na API...')
            res = requests.get(url_api, headers=headers)
            results = res.json()['results']
            if (len(results) > 0):
                print('Consulta realizada com sucesso!')
            else:
                print('Ops! Nenhum dado foi encontrado!')
        except:
            print('Ops! Ocorreu um erro')

        if len(results):
            result = {
                "cidade": results[0]["city"],
                "estado": results[0]["state"],
                "data": results[0]["date"],
                "casos_confirmados": results[0]["last_available_confirmed"],
                "mortes_confirmadas": results[0]["last_available_deaths"],
                "populacao_estimada": results[0]["estimated_population"]
            }
        else:
            result = {
                "cidade": "Não encontrado",
                "estado": "Não encontrado",
                "data": "Não encontrado",
                "casos_confirmados": "Não encontrado",
                "mortes_confirmadas": "Não encontrado",
                "populacao_estimada": "Não encontrado"
            }

        return result


    def read_json(self, file):
        path = dirname(realpath(__file__))
        if isfile(path + file):
            with open(path + file) as f:
                data = load(f)
            return data
        else:
            return False


if __name__ == "__main__":
    ApiService()