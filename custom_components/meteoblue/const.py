"""Constants for the Meteoblue Weather integration."""

DOMAIN = "meteoblue"

CONF_API_KEY = "api_key"
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"

DEFAULT_NAME = "Meteoblue"

# Map Meteoblue pictocodes to Home Assistant weather conditions
# See: https://content.meteoblue.com/en/help/standards/weather-variables/weather-pictograms
PICTOCODE_CONDITION_MAP = {
    1: "sunny",
    2: "partlycloudy",
    3: "cloudy",
    4: "cloudy",
    5: "cloudy",
    6: "fog",
    7: "rainy",
    8: "snowy",
    9: "fog",
    10: "rainy",
    11: "snowy",
    12: "rainy",
    13: "snowy",
    14: "snowy-rainy",
    15: "rainy",
    16: "snowy",
    17: "snowy-rainy",
    18: "rainy",
    19: "snowy",
    20: "snowy-rainy",
    21: "lightning-rainy",
    22: "lightning-rainy",
    23: "lightning-rainy",
    24: "lightning-rainy",
    25: "rainy",
    26: "snowy",
    27: "snowy-rainy",
}

