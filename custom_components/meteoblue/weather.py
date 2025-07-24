from homeassistant.components.weather import WeatherEntity, WeatherEntityFeature
from homeassistant.components.weather.const import (
    UnitOfTemperature, UnitOfSpeed, UnitOfLength, WeatherCondition
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from .coordinator import MeteoblueDataUpdateCoordinator

CONDITION_MAP = {
    "clear": WeatherCondition.SUNNY,
    "partly": WeatherCondition.PARTLYCLOUDY,
    "cloudy": WeatherCondition.CLOUDY,
    "rain": WeatherCondition.RAINY,
    "snow": WeatherCondition.SNOWY,
    "storm": WeatherCondition.LIGHTNING,
    "fog": WeatherCondition.FOG,
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator = MeteoblueDataUpdateCoordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([MeteoblueWeather(coordinator)], False)

class MeteoblueWeather(CoordinatorEntity, WeatherEntity):
    _attr_supported_features = WeatherEntityFeature.FORECAST_DAILY

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "Meteoblue Weather"
        self._attr_native_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_native_wind_speed_unit = UnitOfSpeed.KILOMETERS_PER_HOUR
        self._attr_native_visibility_unit = UnitOfLength.KILOMETERS

    @property
    def condition(self):
        raw = self.coordinator.data["data"]["weather"]["value"][0]
        return CONDITION_MAP.get(raw, WeatherCondition.UNKNOWN)

    @property
    def temperature(self):
        return self.coordinator.data["data"]["temperature"]["value"][0]

    @property
    def wind_speed(self):
        return self.coordinator.data["data"]["windspeed"]["value"][0]

    @property
    def humidity(self):
        return self.coordinator.data["data"]["relativehumidity"]["value"][0]

    @property
    def forecast(self):
        data = self.coordinator.data["data"]
        times = data["temperature"]["value"]
        conds = data["weather"]["value"]
        return [
            {"datetime": self.coordinator.data["metadata"]["modelrun_utc"], "temperature": times[i], "condition": CONDITION_MAP.get(conds[i], WeatherCondition.UNKNOWN)}
            for i in range(min(len(times), len(conds)))
        ]
