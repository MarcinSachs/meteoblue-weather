import aiohttp, async_timeout
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE

class MeteoblueDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config):
        super().__init__(
            hass,
            hass.logger,
            name=DOMAIN,
            update_interval=timedelta(minutes=60),
        )
        self.api_key = config[CONF_API_KEY]
        self.lat = config[CONF_LATITUDE]
        self.lon = config[CONF_LONGITUDE]

    async def _async_update_data(self):
        url = f"https://my.meteoblue.com/packages/basic-1h?apikey={self.api_key}&lat={self.lat}&lon={self.lon}&format=json"
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(15):
                resp = await session.get(url)
                resp.raise_for_status()
                return await resp.json()
