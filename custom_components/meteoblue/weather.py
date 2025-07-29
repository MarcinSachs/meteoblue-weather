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
