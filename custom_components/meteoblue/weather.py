from homeassistant.components.weather import Forecast, WeatherEntity, WeatherEntityFeature
from homeassistant.const import UnitOfLength, UnitOfPressure, UnitOfSpeed, UnitOfTemperature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MeteoblueDataUpdateCoordinator

HOURLY_PICTOCODE_CONDITION_MAP = {
    1: "sunny",
    2: "sunny",
    3: "sunny",
    4: "partlycloudy",
    5: "partlycloudy",
    6: "partlycloudy",
    7: "partlycloudy",
    8: "partlycloudy",
    9: "partlycloudy",
    10: "lightning",
    11: "lightning",
    12: "lightning",
    13: "fog",
    14: "fog",
    15: "fog",
    16: "fog",
    17: "fog",
    18: "fog",
    19: "cloudy",
    20: "cloudy",
    21: "cloudy",
    22: "cloudy",
    23: "rainy",
    24: "snowy",
    25: "pouring",
    26: "snowy",
    27: "lightning-rainy",
    28: "lightning-rainy",
    29: "snowy",
    30: "lightning-rainy",
    31: "snowy-rainy",
    32: "snowy",
    33: "rainy",
    34: "snowy",
    35: "snowy-rainy",
}

DAILY_PICTOCODE_CONDITION_MAP = {
    1: "sunny",
    2: "partlycloudy",
    3: "partlycloudy",
    4: "cloudy",
    5: "fog",
    6: "rainy",
    7: "rainy",
    8: "lightning-rainy",
    9: "snowy",
    10: "snowy",
    11: "snowy-rainy",
    12: "rainy",
    13: "snowy",
    14: "rainy",
    15: "snowy",
    16: "rainy",
    17: "snowy",
}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator: MeteoblueDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MeteoblueWeather(coordinator, entry)])


class MeteoblueWeather(CoordinatorEntity, WeatherEntity):
    _attr_supported_features = WeatherEntityFeature.FORECAST_DAILY | WeatherEntityFeature.FORECAST_HOURLY

    def __init__(self, coordinator: MeteoblueDataUpdateCoordinator, entry: ConfigEntry):
        super().__init__(coordinator)
        self._attr_name = entry.title
        self._attr_native_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_native_pressure_unit = UnitOfPressure.HPA
        self._attr_native_wind_speed_unit = UnitOfSpeed.KILOMETERS_PER_HOUR
        self._attr_native_visibility_unit = UnitOfLength.KILOMETERS
        self._attr_unique_id = entry.unique_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=entry.title,
            manufacturer="Meteoblue",
            entry_type="service",
        )

    @property
    def condition(self):
        code = self.coordinator.data["data_1h"]["pictocode"][0]
        return HOURLY_PICTOCODE_CONDITION_MAP.get(code, "unknown")

    @property
    def native_temperature(self):
        return self.coordinator.data["data_1h"]["temperature"][0]

    @property
    def native_pressure(self):
        return self.coordinator.data["data_1h"]["sealevelpressure"][0]

    @property
    def native_wind_speed(self):
        return self.coordinator.data["data_1h"]["windspeed"][0]

    @property
    def humidity(self):
        return self.coordinator.data["data_1h"]["relativehumidity"][0]

    def _build_forecast(self, data, *, daily):
        mapper = DAILY_PICTOCODE_CONDITION_MAP if daily else HOURLY_PICTOCODE_CONDITION_MAP
        forecasts: list[Forecast] = []
        if daily:
            for time, t_max, t_min, code in zip(data["time"], data["temperature_max"], data["temperature_min"], data["pictocode"]):
                forecasts.append({"datetime": time, "native_temperature": t_max, "native_templow": t_min, "condition": mapper.get(code, "unknown")})
        else:
            for time, temp, code in zip(data["time"], data["temperature"], data["pictocode"]):
                forecasts.append({"datetime": time, "native_temperature": temp, "condition": mapper.get(code, "unknown")})
        return forecasts

    async def async_forecast_daily(self):
        return self._build_forecast(self.coordinator.data["data_day"], daily=True)

    async def async_forecast_hourly(self):
        return self._build_forecast(self.coordinator.data["data_1h"], daily=False)
