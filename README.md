
<div align="center">

   <h1>Meteoblue Weather for Home Assistant</h1>
   
</div>

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

The **Meteoblue Weather** integration for Home Assistant allows you to retrieve detailed weather data directly from the Meteoblue API.

## Key Features

*   Current weather conditions.
*   Hourly and daily forecasts.
*   Full integration with the Lovelace weather card.
*   Supports both free and commercial API keys (using `Shared Secret`).

## Installation

### Method 1: HACS (Recommended)

This is the easiest method and ensures you get automatic updates.

1.  Ensure you have HACS installed.
2.  Go to **HACS > Integrations**.
3.  Click the 3 dots in the top right corner and select **Custom repositories**.
4.  Paste the URL of this repository into the "Repository" field, select the "Integration" category, and click **ADD**.
5.  Find the "Meteoblue Weather" integration in the list and click **INSTALL**.

You can also add the repository to HACS by clicking the button below:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=MarcinSachs&repository=meteoblue-weather&category=integration)


### Method 2: Manual Installation

1.  Download the latest version of the integration from the "Releases" tab on GitHub.
2.  Unpack the archive.
3.  Copy the `custom_components/meteoblue` folder to the `custom_components` folder in your Home Assistant installation.
4.  Restart Home Assistant.

## Configuration

After installing the integration, the configuration is done through the user interface.

1.  Go to **Settings > Devices & Services > Integrations**.
2.  Click **Add Integration** and search for "Meteoblue".
3.  Fill out the configuration form:
    *   **Name**: A friendly name for this instance (e.g., "Home Weather").
    *   **API Key**: Your API key from the Meteoblue service.
    *   **Latitude**: The latitude of the location (defaults to HA settings).
    *   **Longitude**: The longitude of the location (defaults to HA settings).
    *   **Shared Secret (optional)**: If you are using a paid package with request signing, enter your "shared secret" here.

After successful configuration, a new `weather` entity will be created.

## API

This integration uses the Meteoblue API. An API key is required for it to work.

## Special Thanks

[dnesdan](https://github.com/dnesdan)

