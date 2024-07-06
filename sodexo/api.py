import requests

class SodexoAPI:
    def __init__(self, username, password):
        self.base_url = "https://connect.pluxee.app/op/interaction/"
        self.session = requests.Session()
        self.token = None
        self.login(username, password)

    def login(self, username, password):
        try:
            login_url = self.base_url + "Gm-k-neDeJp0csiBIEsok"
            response = self.session.post(login_url, data={"username": username, "password": password})
            response.raise_for_status()
            data = response.json()
            self.token = data.get("access_token")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao fazer login: {e}")
            raise

    def get_balance(self):
        if not self.token:
            raise ValueError("Token não encontrado. Certifique-se de que o login foi realizado com sucesso.")
        try:
            balance_url = self.base_url + "balance"
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.session.get(balance_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("balance")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter saldo: {e}")
            raise
        except ValueError as e:
            print(f"Erro ao processar resposta: {e}")
            raise
