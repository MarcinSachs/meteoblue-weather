from homeassistant.components.weather import WeatherEntity
from homeassistant.const import TEMP_CELSIUS, LENGTH_KILOMETERS, SPEED_KILOMETERS_PER_HOUR
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import aiohttp
import async_timeout
from datetime import timedelta, datetime

from .const import CONF_API_KEY, CONF_LATITUDE, CONF_LONGITUDE, DOMAIN

CONDITION_MAP = {
    "clear": "sunny",
    "partly": "partlycloudy",
    "cloudy": "cloudy",
    "rain": "rainy",
    "snow": "snowy",
    "storm": "lightning",
    "fog": "fog",
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coords = entry.data
    coordinator = MeteoblueDataUpdateCoordinator(hass, coords)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([MeteoblueWeather(coordinator)], False)


class MeteoblueDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config):
        super().__init__(
            hass,
            _LOGGER := hass.logger,
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


class MeteoblueWeather(CoordinatorEntity, WeatherEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Meteoblue Weather"
        self._attr_native_temperature_unit = TEMP_CELSIUS
        self._attr_native_wind_speed_unit = SPEED_KILOMETERS_PER_HOUR
        self._attr_native_visibility_unit = LENGTH_KILOMETERS

    @property
    def temperature(self):
        return self._get("temperature", 0)

    @property
    def wind_speed(self):
        return self._get("windspeed", 0)

    @property
    def condition(self):
        raw = self._get("weather", 0)
        return CONDITION_MAP.get(raw, "unknown")

    @property
    def humidity(self):
        return self._get("relativehumidity", 0)

    @property
    def forecast(self):
        data = self.coordinator.data["data"]
        times = data["temperature"]["value"]
        weathers = data["weather"]["value"]
        now = datetime.utcnow()
        return [
            {"datetime": now + timedelta(
                hours=i), "temperature": times[i], "condition": CONDITION_MAP.get(weathers[i], "unknown")}
            for i in range(min(len(times), len(weathers)))
        ]

    def _get(self, key, default):
        return self.coordinator.data["data"].get(key, {}).get("value", [default])[0]
