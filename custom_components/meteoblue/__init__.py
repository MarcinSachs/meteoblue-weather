"""The Meteoblue Weather integration."""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "meteoblue"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    await hass.config_entries.async_forward_entry_setups(entry, ["weather"])
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, ["weather"])
