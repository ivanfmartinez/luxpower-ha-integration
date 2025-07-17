import asyncio
import logging
from .const import *

from .services.poll_service import poll_inverter_task

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Unused for UI config."""
    return True


async def async_setup_entry(hass, entry):
    """Set up from a config entry."""
    _LOGGER.info("%s: Initializing from UI config.", INTEGRATION_TITLE)
    hass.data.setdefault(DOMAIN, {})
    settings = {**entry.data, **entry.options}
    lock = asyncio.Lock()

    # Pre-create the full data structure for this entry
    hass.data[DOMAIN][entry.entry_id] = {
        "settings": settings,
        "registers": {"input": {}, "hold": {}},
        "initialized": False,
        "lock": lock
    }

    host = settings[CONF_HOST]
    port = settings[CONF_PORT]
    dongle_serial = settings[CONF_DONGLE_SERIAL]
    inverter_serial = settings[CONF_INVERTER_SERIAL]
    poll_interval = int(settings.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL))

    # Start polling background task and store it so we can cancel it later
    task = hass.loop.create_task(
        poll_inverter_task(hass, entry, host, port, dongle_serial.encode(), inverter_serial.encode(), poll_interval,
                           lock)
    )
    hass.data[DOMAIN][entry.entry_id]["poll_task"] = task

    # Forward the setup to the platforms (sensor, number, etc.)
    # This now happens immediately without waiting for the first poll.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    # 1. Cancel the background polling task
    poll_task = hass.data[DOMAIN][entry.entry_id].get("poll_task")
    if poll_task:
        poll_task.cancel()
        try:
            await poll_task
        except asyncio.CancelledError:
            _LOGGER.debug("Polling task successfully cancelled.")

    # 2. Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # 3. Remove data for this entry
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
