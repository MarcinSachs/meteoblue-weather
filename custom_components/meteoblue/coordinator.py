import aiohttp, async_timeout
from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import hashlib
import hmac
import time

from .const import DOMAIN, CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE, CONF_SHARED_SECRET

_LOGGER = logging.getLogger(__name__)

class MeteoblueDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=60),
        )
        self.api_key = config[CONF_API_KEY]
        self.lat = config[CONF_LATITUDE]
        self.lon = config[CONF_LONGITUDE]
        self.shared_secret = config.get(CONF_SHARED_SECRET)

    async def _async_update_data(self):
        packages = "basic-1h_basic-day"
        if self.shared_secret:
            expire = int(time.time()) + 600
            query = f"/packages/{packages}?lat={self.lat}&lon={self.lon}&apikey={self.api_key}&expire={expire}&format=json"
            signature = hmac.new(self.shared_secret.encode(), query.encode(), hashlib.sha256).hexdigest()
            url = f"https://my.meteoblue.com{query}&sig={signature}"
        else:
            url = f"https://my.meteoblue.com/packages/{packages}?apikey={self.api_key}&lat={self.lat}&lon={self.lon}&format=json"
            
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(15):
                resp = await session.get(url)
                resp.raise_for_status()
                return await resp.json()