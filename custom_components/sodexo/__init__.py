from homeassistant.helpers import config_entry_flow

from .const import DOMAIN

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    hass.data[DOMAIN] = entry.data
    return True

async def async_unload_entry(hass, entry):
    hass.data.pop(DOMAIN)
    return True
