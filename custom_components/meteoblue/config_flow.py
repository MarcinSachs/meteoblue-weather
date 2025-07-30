from homeassistant import config_entries
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN, CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE, CONF_SHARED_SECRET, CONF_NAME

class MeteoblueConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            unique_id = f"{user_input[CONF_LATITUDE]}-{user_input[CONF_LONGITUDE]}"
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_NAME, default=self.hass.config.location_name): str,
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_LATITUDE, default=self.hass.config.latitude): cv.latitude,
                vol.Required(CONF_LONGITUDE, default=self.hass.config.longitude): cv.longitude,
                vol.Optional(CONF_SHARED_SECRET): str,
            }),
            errors=errors,
        )