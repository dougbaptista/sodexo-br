import requests
from bs4 import BeautifulSoup

class SodexoAPI:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.base_url = "https://connect.pluxee.app/op/interaction/"
        self.login_url = "https://b2c.sodexobeneficios.com.br/login/"
        self.token = None
        self.authenticate()

    def get_initial_token(self):
        response = self.session.get(self.login_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        token_input = soup.find('input', {'name': 'token'})
        if token_input:
            return token_input['value']
        raise ValueError("Não foi possível obter o token inicial.")

    def authenticate(self):
        try:
            token = self.get_initial_token()
            interaction_url = self.base_url + token
            response = self.session.get(interaction_url)
            response.raise_for_status()

            login_data = {
                "username": self.username,
                "continue": "Continue"  # Nome do botão continuar pode variar
            }
            login_response = self.session.post(interaction_url, data=login_data)
            login_response.raise_for_status()

            password_data = {
                "password": self.password,
                "continue": "Continue"
            }
            password_response = self.session.post(interaction_url, data=password_data)
            password_response.raise_for_status()

            # Verificar se o login foi bem-sucedido
            if "error" in password_response.url:
                raise ValueError("Erro de autenticação: verifique suas credenciais.")

            # A partir daqui, você deve ter um token válido na sessão
            self.token = self.session.cookies.get('token')
            if not self.token:
                raise ValueError("Token não encontrado após login.")
        
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
            print(f"Erro ao processar resposta do saldo: {e}")
            raise
