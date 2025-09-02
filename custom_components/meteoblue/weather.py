<<<<<<< HEAD
<<<<<<< HEAD
"""Weather platform for Meteoblue."""
from homeassistant.components.weather import (
    ATTR_FORECAST_CONDITION,
    ATTR_FORECAST_NATIVE_TEMP,
    ATTR_FORECAST_NATIVE_TEMP_LOW,
    ATTR_FORECAST_PRECIPITATION_PROBABILITY,
    ATTR_FORECAST_TIME,
    WeatherEntity,
)
from homeassistant.const import UnitOfSpeed, UnitOfTemperature
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN, PICTOCODE_CONDITION_MAP


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Meteoblue weather platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([MeteoblueWeather(coordinator, entry.title)])


class MeteoblueWeather(CoordinatorEntity, WeatherEntity):
    """Representation of a weather entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, name):
        """Initialize the Meteoblue weather entity."""
        super().__init__(coordinator)
        # The entity name will be "Weather". HA will combine it with the device name.
        self._attr_name = "Weather"
        self._attr_native_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_native_wind_speed_unit = UnitOfSpeed.KILOMETERS_PER_HOUR
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name=name,
            manufacturer="meteoblue",
            model="API Forecast",
        )

    @property
    def condition(self):
        """Return the current condition."""
        if not self.coordinator.data or "data_current" not in self.coordinator.data:
            return None
        pictocode = self.coordinator.data["data_current"].get("pictocode")
        if pictocode is None:
            return None
        return PICTOCODE_CONDITION_MAP.get(pictocode, "sunny")

    @property
    def native_temperature(self):
        """Return the temperature."""
        if not self.coordinator.data or "data_current" not in self.coordinator.data:
            return None
        return self.coordinator.data["data_current"].get("temperature")

    @property
    def humidity(self):
        """Return the humidity."""
        if not self.coordinator.data or "data_current" not in self.coordinator.data:
            return None
        return self.coordinator.data["data_current"].get("relativehumidity")

    @property
    def native_wind_speed(self):
        """Return the wind speed."""
        if not self.coordinator.data or "data_current" not in self.coordinator.data:
            return None
        wind_speed_ms = self.coordinator.data["data_current"].get("windspeed")
        if wind_speed_ms is None:
            return None
        # Convert from m/s to km/h
        return round(wind_speed_ms * 3.6, 2)

    @property
    def forecast(self):
        """Return the forecast array."""
        if not self.coordinator.data or "data_day" not in self.coordinator.data:
            return None

        forecast_data = []
        data_day = self.coordinator.data.get("data_day", {})

        # Check if all required forecast keys exist and are lists
        required_keys = [
            "time",
            "temperature_max",
            "temperature_min",
            "precipitation_probability",
            "pictocode",
        ]
        if not all(isinstance(data_day.get(key), list) for key in required_keys):
            return None

        # Find the minimum length of the forecast lists to avoid IndexError
        min_len = min(len(data_day.get(key, [])) for key in required_keys)

        for i in range(min_len):
            pictocode = data_day["pictocode"][i]
            condition = PICTOCODE_CONDITION_MAP.get(pictocode, "sunny")

            forecast_item = {
                ATTR_FORECAST_TIME: data_day["time"][i] + "T12:00:00Z",
                ATTR_FORECAST_NATIVE_TEMP: data_day["temperature_max"][i],
                ATTR_FORECAST_NATIVE_TEMP_LOW: data_day["temperature_min"][i],
                ATTR_FORECAST_PRECIPITATION_PROBABILITY: data_day["precipitation_probability"][i],
                ATTR_FORECAST_CONDITION: condition,
            }
            forecast_data.append(forecast_item)

        return forecast_data

    @property
    def attribution(self):
        """Return the attribution."""
        return "Powered by meteoblue"
=======
from homeassistant.components.weather import WeatherEntity, WeatherEntityFeature
from homeassistant.components.weather.const import (
    UnitOfTemperature, UnitOfSpeed, UnitOfLength, WeatherCondition
)
=======
from homeassistant.components.weather import Forecast, WeatherEntity, WeatherEntityFeature
from homeassistant.const import UnitOfLength, UnitOfPressure, UnitOfSpeed, UnitOfTemperature
>>>>>>> e6664fb28e7788ca18ab812507be815c8f51dbcb
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

<<<<<<< HEAD
    @property
    def forecast(self):
        data = self.coordinator.data["data"]
        times = data["temperature"]["value"]
        conds = data["weather"]["value"]
        return [
            {"datetime": self.coordinator.data["metadata"]["modelrun_utc"], "temperature": times[i], "condition": CONDITION_MAP.get(conds[i], WeatherCondition.UNKNOWN)}
            for i in range(min(len(times), len(conds)))
        ]
>>>>>>> c6ef35ccbca751e4de3d7f341fec45d568017de5
=======
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
>>>>>>> e6664fb28e7788ca18ab812507be815c8f51dbcb
