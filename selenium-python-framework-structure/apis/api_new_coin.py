import logging
import requests


class ApiBraveNewCoinQA:
    def __init__(self):
        logging.info(f"Definiendo el constructor de api new coin")
        self.base_url = "https://bravenewcoin.p.rapidapi.com/"
        self.token = self.__generar_token()

    def __generar_token(self):
        payload = {
            "audience": "https://api.bravenewcoin.com",
            "client_id": "oCdQoZoI96ERE9HY3sQ7JmbACfBf55RY",
            "grant_type": "client_credentials"
        }
        logging.info(f"Intentando hacer post a la api:{'https://bravenewcoin.p.rapidapi.com/oauth/token'} en qa")
        response = requests.post(url='https://bravenewcoin.p.rapidapi.com/oauth/token', headers={}, data=payload,
                                 auth=())
        if response.status_code == 200:
            logging.info(f"Se completó la acción correctamente")
            return response.json()["access_token"]
        else:
            logging.info(f"Falló la accion de completar el token {response.status_code} en qa")
            return False

    def get_token(self):
        return self.token

    def get_validar_status_code(self):
        path = "oauth/token"
        url = self.base_url + path
        payload = {
            "audience": "https://api.bravenewcoin.com",
            "client_id": "oCdQoZoI96ERE9HY3sQ7JmbACfBf55RY",
            "grant_type": "client_credentials"
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": "9466ac8e96msh5fc3fbd86848798p1a7ceajsn76234786571d",
            "X-RapidAPI-Host": "bravenewcoin.p.rapidapi.com"
        }

        response = requests.request("POST", url=url, json=payload, headers=headers)
        return response




