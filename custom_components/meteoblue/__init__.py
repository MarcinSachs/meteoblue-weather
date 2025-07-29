"""The Meteoblue Weather integration."""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import MeteoblueApiClient
from .const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE, DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["weather"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meteoblue Weather from a config entry."""
    session = async_get_clientsession(hass)
    client = MeteoblueApiClient(
        entry.data[CONF_API_KEY],
        entry.data[CONF_LATITUDE],
        entry.data[CONF_LONGITUDE],
        session,
    )

    async def async_update_data():
        """Fetch data from API."""
        try:
            return await client.get_data()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Meteoblue Sensor",
        update_method=async_update_data,
        update_interval=timedelta(minutes=15),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
