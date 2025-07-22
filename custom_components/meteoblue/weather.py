from homeassistant.components.weather import WeatherEntity
from homeassistant.const import TEMP_CELSIUS, LENGTH_KILOMETERS, SPEED_KILOMETERS_PER_HOUR
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import aiohttp
import async_timeout
import logging
from datetime import timedelta, datetime

_LOGGER = logging.getLogger(__name__)

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
    coordinator = MeteoblueDataUpdateCoordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()

    async_add_entities([MeteoblueWeather(coordinator)])

class MeteoblueDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config):
        super().__init__(
            hass,
            _LOGGER,
            name="Meteoblue Weather",
            update_interval=timedelta(minutes=60),
        )
        self.api_key = config["api_key"]
        self.lat = config["latitude"]
        self.lon = config["longitude"]

    async def _async_update_data(self):
        url = f"https://my.meteoblue.com/packages/basic-1h?apikey={self.api_key}&lat={self.lat}&lon={self.lon}&format=json"
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                async with session.get(url) as response:
                    return await response.json()

class MeteoblueWeather(CoordinatorEntity, WeatherEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Meteoblue Weather"
        self._attr_unique_id = "meteoblue_weather"
        self._attr_native_temperature_unit = TEMP_CELSIUS
        self._attr_native_wind_speed_unit = SPEED_KILOMETERS_PER_HOUR
        self._attr_native_visibility_unit = LENGTH_KILOMETERS

    @property
    def temperature(self):
        return self._safe_get(["data", "temperature", "value", 0])

    @property
    def humidity(self):
        return self._safe_get(["data", "relativehumidity", "value", 0])

    @property
    def wind_speed(self):
        return self._safe_get(["data", "windspeed", "value", 0])

    @property
    def condition(self):
        raw = self._safe_get(["data", "weather", "value", 0])
        return CONDITION_MAP.get(raw, None)

    @property
    def forecast(self):
        forecast = []
        timestamps = self._safe_get(["metadata", "modelrun_utc"], fallback=None)
        temps = self._safe_get(["data", "temperature", "value"], fallback=[])
        weathers = self._safe_get(["data", "weather", "value"], fallback=[])

        for i in range(min(len(temps), len(weathers))):
            forecast.append({
                "datetime": datetime.utcnow() + timedelta(hours=i),
                "temperature": temps[i],
                "condition": CONDITION_MAP.get(weathers[i], None),
            })
        return forecast

    def _safe_get(self, path, fallback=None):
        data = self.coordinator.data
        for p in path:
            if isinstance(data, dict) and p in data:
                data = data[p]
            else:
                return fallback
        return data