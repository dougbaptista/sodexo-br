from homeassistant.helpers.entity import Entity
from .api import SodexoAPI

def setup_platform(hass, config, add_entities, discovery_info=None):
    username = config.get("username")
    password = config.get("password")

    api = SodexoAPI(username, password)
    add_entities([SodexoBalanceSensor(api)], True)

class SodexoBalanceSensor(Entity):
    def __init__(self, api):
        self.api = api
        self._state = None

    @property
    def name(self):
        return "Saldo Sodexo"

    @property
    def state(self):
        return self._state

    def update(self):
        try:
            self._state = self.api.get_balance()
        except Exception as e:
            print(f"Erro ao atualizar sensor: {e}")
            self._state = None
