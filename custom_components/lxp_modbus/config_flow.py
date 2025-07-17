import voluptuous as vol
import asyncio
import logging

from .utils import decode_model_from_registers
from homeassistant import config_entries

from .const import *

from .classes.lxp_request_builder import LxpRequestBuilder
from .classes.lxp_response import LxpResponse

_LOGGER = logging.getLogger(__name__)

MINOR_VERSION = "MINOR"
FULL_TITLE = f"{INTEGRATION_TITLE} (Version 0.1.0 {MINOR_VERSION})"

def validate_serial(value):
    value = str(value)
    if len(value) != 10:
        raise vol.Invalid("Must be exactly 10 characters.")
    return value

async def get_inverter_model_from_device(host, port, dongle_serial, inverter_serial):
    try:
        reader, writer = await asyncio.open_connection(host, port)
        _LOGGER.debug(f"Connecting to inverter at {host}:{port}")
        req = LxpRequestBuilder.prepare_packet_for_read(
            dongle_serial.encode(), inverter_serial.encode(), 7, 2, 3  # 0x03 = HOLD registers, read 2 registers
        )
        writer.write(req)
        await writer.drain()
        _LOGGER.debug("Modbus request sent, waiting for response")
        response_buf = await reader.read(512)
        writer.close()
        await writer.wait_closed()
        if not response_buf:
            _LOGGER.error("No response from inverter")
            return None
        response = LxpResponse(response_buf)
        if response.packet_error:
            _LOGGER.error("LxpResponse reports packet error")
            return None
        _LOGGER.debug(f"Response dict: {response.parsed_values_dictionary}")
        # Now use only registers 7 and 8
        model = decode_model_from_registers(response.parsed_values_dictionary)
        _LOGGER.info(f"Read inverter model: {model!r}")
        return model
    except Exception as ex:
        _LOGGER.error(f"Exception in model fetch: {ex}")
        return None

class MyModbusBridgeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            try:
                user_input[CONF_DONGLE_SERIAL] = validate_serial(user_input[CONF_DONGLE_SERIAL])
            except vol.Invalid as ex:
                errors[CONF_DONGLE_SERIAL] = str(ex)
            try:
                user_input[CONF_INVERTER_SERIAL] = validate_serial(user_input[CONF_INVERTER_SERIAL])
            except vol.Invalid as ex:
                errors[CONF_INVERTER_SERIAL] = str(ex)
            if not errors:
                entry_title = user_input.get(CONF_ENTITY_PREFIX, DEFAULT_ENTITY_PREFIX)
                # Fetch model
                model = await get_inverter_model_from_device(
                    user_input[CONF_HOST],
                    user_input[CONF_PORT],
                    user_input[CONF_DONGLE_SERIAL],
                    user_input[CONF_INVERTER_SERIAL]
                )
                if not model:
                    errors["base"] = "model_fetch_failed"
                else:
                    user_input["model"] = model
                    return self.async_create_entry(title=entry_title, data=user_input)

        data_schema = vol.Schema({
            vol.Required(CONF_HOST, default=""): str,
            vol.Required(CONF_PORT, default=8000): int,
            vol.Required(CONF_DONGLE_SERIAL, default=""): str,
            vol.Required(CONF_INVERTER_SERIAL, default=""): str,
            vol.Required(CONF_POLL_INTERVAL, default=DEFAULT_POLL_INTERVAL): vol.All(int, vol.Range(min=2, max=600)),
            vol.Required(CONF_ENTITY_PREFIX, default=DEFAULT_ENTITY_PREFIX): str,
            vol.Required(CONF_RATED_POWER, default=DEFAULT_RATED_POWER): vol.All(int, vol.Range(1000, 100000)),
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "model_fetch_failed": "Could not read inverter model (registers 7–8). Check connection/settings."
            }
        )

    async def async_step_reconfigure(self, user_input=None):
        errors = {}
        entry = self._get_reconfigure_entry()
        defaults = entry.data.copy()
        defaults.update(entry.options or {})

        if user_input is not None:
            try:
                user_input[CONF_DONGLE_SERIAL] = validate_serial(user_input[CONF_DONGLE_SERIAL])
            except vol.Invalid as ex:
                errors[CONF_DONGLE_SERIAL] = str(ex)
            try:
                user_input[CONF_INVERTER_SERIAL] = validate_serial(user_input[CONF_INVERTER_SERIAL])
            except vol.Invalid as ex:
                errors[CONF_INVERTER_SERIAL] = str(ex)
            if not errors:
                # Fetch model again in case serials/host/port have changed
                model = await get_inverter_model_from_device(
                    user_input[CONF_HOST],
                    user_input[CONF_PORT],
                    user_input[CONF_DONGLE_SERIAL],
                    user_input[CONF_INVERTER_SERIAL]
                )
                if not model:
                    errors["base"] = "model_fetch_failed"
                else:
                    user_input["model"] = model
                    return self.async_update_reload_and_abort(
                        entry,
                        data_updates=user_input,
                    )

        data_schema = vol.Schema({
            vol.Required(CONF_HOST, default=defaults.get(CONF_HOST, "")): str,
            vol.Required(CONF_PORT, default=defaults.get(CONF_PORT, 8000)): int,
            vol.Required(CONF_DONGLE_SERIAL, default=defaults.get(CONF_DONGLE_SERIAL, "")): str,
            vol.Required(CONF_INVERTER_SERIAL, default=defaults.get(CONF_INVERTER_SERIAL, "")): str,
            vol.Required(CONF_POLL_INTERVAL, default=defaults.get(CONF_POLL_INTERVAL, DEFAULT_POLL_INTERVAL)): vol.All(int, vol.Range(min=2, max=600)),
            vol.Required(CONF_ENTITY_PREFIX, default=defaults.get(CONF_ENTITY_PREFIX, DEFAULT_ENTITY_PREFIX)): str,
            vol.Required(CONF_RATED_POWER, default=5000): vol.All(int, vol.Range(1000, 100000)),
        })

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "model_fetch_failed": "Could not read inverter model (registers 7–10). Check connection/settings."
            }
        )
