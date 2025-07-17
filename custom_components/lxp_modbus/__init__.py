import asyncio
import logging
from .const import *

from .services.poll_service import poll_inverter_task
from .classes.lxp_request_builder import LxpRequestBuilder
from .classes.lxp_response import LxpResponse

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    """Unused for UI config."""
    return True

async def async_setup_entry(hass, entry):
    """Set up from a config entry."""
    _LOGGER.info("%s: Initializing from UI config.", INTEGRATION_TITLE)
    hass.data.setdefault(DOMAIN, {})
    settings = {**entry.data, **entry.options}
    hass.data[DOMAIN][entry.entry_id] = settings
    hass.data[DOMAIN][entry.entry_id]['initialized'] = False

    # --- ADD THIS: Pre-create the 'registers' structure ---
    if "registers" not in hass.data[DOMAIN][entry.entry_id]:
        hass.data[DOMAIN][entry.entry_id]["registers"] = {
            "input": {},
            "hold": {},
        }
    
    host = settings[CONF_HOST]
    port = settings[CONF_PORT]
    dongle_serial = settings[CONF_DONGLE_SERIAL].encode()
    inverter_serial = settings[CONF_INVERTER_SERIAL].encode()
    poll_interval = int(settings.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL))
    entity_prefix = entry.data.get(CONF_ENTITY_PREFIX, DEFAULT_ENTITY_PREFIX)
    rated_power = int(settings.get(CONF_RATED_POWER,DEFAULT_RATED_POWER))

    # Start polling background task
    task = hass.loop.create_task(
        poll_inverter_task(hass, entry, host, port, dongle_serial, inverter_serial, poll_interval)
    )
    
    while not hass.data[DOMAIN][entry.entry_id].get('initialized', False):
        await asyncio.sleep(10)  # Sleep for 10 seconds
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass, entry):
    # 1. Cancel background polling tasks
    poll_task = hass.data[DOMAIN][entry.entry_id].get("poll_task")
    if poll_task:
        poll_task.cancel()
        try:
            await poll_task
        except asyncio.CancelledError:
            pass

    # 2. Remove data
    hass.data[DOMAIN].pop(entry.entry_id, None)

    # 3. Unload platforms
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)  # add your platforms

    return unload_ok