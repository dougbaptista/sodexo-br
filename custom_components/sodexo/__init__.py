import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from homeassistant.helpers import config_entry_flow
from .const import DOMAIN

async def async_setup(hass, config):
    # Configurar a tradução fixa para PT-BR
    hass.config.api.language = 'pt-BR'
    return True

async def async_setup_entry(hass, entry):
    # Configurar a tradução fixa para PT-BR
    hass.config.api.language = 'pt-BR'
    hass.data[DOMAIN] = entry.data
    return True

async def async_unload_entry(hass, entry):
    hass.data.pop(DOMAIN)
    return True
