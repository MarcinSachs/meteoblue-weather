"""API Client for Meteoblue."""
import asyncio
import logging

import async_timeout
from aiohttp import ClientError, ClientSession

_LOGGER = logging.getLogger(__name__)


class MeteoblueApiClient:
    """Meteoblue API Client."""

    def __init__(
        self,
        apikey: str,
        latitude: float,
        longitude: float,
        session: ClientSession,
    ):
        """Initialize the API client."""
        self._apikey = apikey
        self._latitude = latitude
        self._longitude = longitude
        self._session = session
        # Request packages for current weather and daily forecast
        packages = "current_basic-day"
        self.base_url = f"https://my.meteoblue.com/packages/{packages}?lat={self._latitude}&lon={self._longitude}&apikey={self._apikey}&format=json"

    async def get_data(self) -> dict:
        """Get data from the Meteoblue API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(self.base_url)
                response.raise_for_status()
                data = await response.json()

                # A valid response should have a 'metadata' key.
                if "metadata" not in data:
                    _LOGGER.error(
                        "Invalid API response (missing metadata): %s", data)
                    raise ClientError(
                        "Meteoblue API response is missing 'metadata'")

                # Also validate that the core data packages we need are present.
                if "data_current" not in data or "data_day" not in data:
                    _LOGGER.error(
                        "API response missing required data ('data_current' or 'data_day'): %s", data)
                    raise ClientError(
                        "Meteoblue API response is missing required data packages")

                _LOGGER.debug("Successfully fetched data: %s", data)
                return data
        except (asyncio.TimeoutError, ClientError) as error:
            _LOGGER.error("Error fetching data from Meteoblue: %s", error)
            raise
