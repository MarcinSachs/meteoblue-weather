"""Config flow for Meteoblue Weather integration."""
import logging

import voluptuous as vol
from aiohttp import ClientError
from homeassistant import config_entries, core, exceptions
from homeassistant.const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import MeteoblueApiClient
from .const import DOMAIN, CONF_NAME

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: core.HomeAssistant, data: dict) -> dict:
    """Validate the user input allows us to connect."""
    session = async_get_clientsession(hass)
    client = MeteoblueApiClient(
        data[CONF_API_KEY], data[CONF_LATITUDE], data[CONF_LONGITUDE], session
    )

    try:
        api_data = await client.get_data()
        # Use the location name from metadata, or create one if it's empty
        title = api_data["metadata"].get("name")
        if not title:
            title = f"Meteoblue ({data[CONF_LATITUDE]:.2f}, {data[CONF_LONGITUDE]:.2f})"
        return {"title": title}
    except ClientError:
        raise CannotConnect
    except Exception:
        _LOGGER.exception("Unexpected exception")
        raise InvalidAuth


@config_entries.HANDLERS.register(DOMAIN)
class MeteoblueConfigFlow(config_entries.ConfigFlow):
    """Handle a config flow for Meteoblue Weather."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Optional(
                    CONF_LATITUDE, default=self.hass.config.latitude
                ): vol.All(vol.Coerce(float), vol.Range(min=-90, max=90)),
                vol.Optional(
                    CONF_LONGITUDE, default=self.hass.config.longitude
                ): vol.All(vol.Coerce(float), vol.Range(min=-180, max=180)),
                vol.Optional(
                    CONF_NAME, default="Meteoblue"
                ): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate there is invalid auth."""
