from homeassistant import config_entries
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from .const import DOMAIN, CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE

class MeteoblueConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input:
            return self.async_create_entry(title="Meteoblue", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_LATITUDE, default=0.0): cv.latitude,
                vol.Required(CONF_LONGITUDE, default=0.0): cv.longitude,
            }),
        )
