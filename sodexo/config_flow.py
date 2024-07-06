import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD

from .const import DOMAIN
from .api import SodexoAPI

@callback
def configured_instances(hass):
    """Retorna um conjunto de instâncias Sodexo configuradas."""
    return set(entry.title for entry in hass.config_entries.async_entries(DOMAIN))

class SodexoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Gerencia o fluxo de configuração para Sodexo."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Gerencia a etapa inicial do fluxo de configuração."""
        errors = {}
        if user_input is not None:
            username = user_input[CONF_USERNAME]
            password = user_input[CONF_PASSWORD]
            try:
                api = SodexoAPI(username, password)
                api.login(username, password)
                return self.async_create_entry(title=username, data=user_input)
            except Exception:
                errors["base"] = "auth"

        data_schema = vol.Schema({
            vol.Required(CONF_USERNAME): str,
            vol.Required(CONF_PASSWORD): str
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    async def async_step_import(self, user_input=None):
        """Importa uma entrada de configuração do configuration.yaml."""
        return await self.async_step_user(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SodexoOptionsFlow(config_entry)

class SodexoOptionsFlow(config_entries.OptionsFlow):
    """Gerencia o fluxo de opções para Sodexo."""

    def __init__(self, config_entry):
        """Inicializa o fluxo de opções."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Gerencia as opções."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Optional("option1", default=self.config_entry.options.get("option1", "")): str
        })

        return self.async_show_form(step_id="init", data_schema=options_schema)
