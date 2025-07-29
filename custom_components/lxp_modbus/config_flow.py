import asyncio
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import *
from .classes.lxp_request_builder import LxpRequestBuilder
from .classes.lxp_response import LxpResponse
from .utils import decode_model_from_registers

_LOGGER = logging.getLogger(__name__)

def validate_serial(value):
    """Validate that the serial number is exactly 10 characters."""
    value = str(value)
    if len(value) != 10:
        raise vol.Invalid("Serial number must be exactly 10 characters.")
    return value

async def get_inverter_model_from_device(host, port, dongle_serial, inverter_serial):
    """Attempt to connect to the inverter and read the model from registers 7-8."""
    try:
        # Open a network connection to the inverter's dongle
        reader, writer = await asyncio.open_connection(host, port)
        # Prepare the Modbus request packet to read 2 HOLD registers starting from address 7
        req = LxpRequestBuilder.prepare_packet_for_read(dongle_serial.encode(), inverter_serial.encode(), 7, 2, 3)
        writer.write(req)
        await writer.drain()
        # Read the response from the socket
        response_buf = await reader.read(512)
        writer.close()
        await writer.wait_closed()
        # If no response, return None
        if not response_buf: return None
        # Parse the raw response bytes
        response = LxpResponse(response_buf)
        # If the packet is corrupted or invalid, return None
        if response.packet_error: return None
        # Decode the model string from the register values
        model = decode_model_from_registers(response.parsed_values_dictionary)
        return model
    except Exception:
        return None

class LxpModbusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial setup flow for the component."""
    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Link to the Options Flow handler for reconfiguration."""
        return LxpModbusOptionsFlow(config_entry)

    async def async_step_user(self, user_input=None):
        """Handle the first step of the user configuration."""
        errors = {}
        # This block runs when the user submits the form
        if user_input is not None:
            try:
                # Validate the serial numbers
                validate_serial(user_input[CONF_DONGLE_SERIAL])
                validate_serial(user_input[CONF_INVERTER_SERIAL])
                # Try to connect to the inverter and get the model
                model = await get_inverter_model_from_device(user_input[CONF_HOST], user_input[CONF_PORT], user_input[CONF_DONGLE_SERIAL], user_input[CONF_INVERTER_SERIAL])
                if not model:
                    # If model fetch fails, show an error and display the form again
                    errors["base"] = "model_fetch_failed"
                else:
                    # If successful, add the model to the data and create the config entry
                    user_input["model"] = model
                    title = user_input.get(CONF_ENTITY_PREFIX) or "Luxpower Inverter"
                    return self.async_create_entry(title=title, data=user_input)
            except vol.Invalid:
                errors["base"] = "invalid_serial"

        # Define the schema for the form fields (without default values)
        data_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PORT): int,
            vol.Required(CONF_DONGLE_SERIAL): str,
            vol.Required(CONF_INVERTER_SERIAL): str,
            vol.Required(CONF_POLL_INTERVAL): vol.All(int, vol.Range(min=2, max=600)),
            vol.Optional(CONF_ENTITY_PREFIX): str,
            vol.Required(CONF_RATED_POWER): vol.All(int, vol.Range(min=1000, max=100000)),
            vol.Optional(CONF_READ_ONLY): bool,
        })
        
        # Create a dictionary of default values to pre-fill the form
        suggested_values = {
            CONF_PORT: DEFAULT_PORT,
            CONF_POLL_INTERVAL: DEFAULT_POLL_INTERVAL,
            CONF_ENTITY_PREFIX: DEFAULT_ENTITY_PREFIX,
            CONF_RATED_POWER: DEFAULT_RATED_POWER,
            CONF_READ_ONLY: DEFAULT_READ_ONLY,
        }

        # Show the form to the user, pre-filled with suggested values
        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(data_schema, suggested_values),
            errors=errors,
        )

class LxpModbusOptionsFlow(config_entries.OptionsFlow):
    """Handle the options flow (reconfiguration) for the component."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options."""
        errors = {}
        
        # This block runs when the user submits the options form
        if user_input is not None:
            try:
                validate_serial(user_input[CONF_DONGLE_SERIAL])
                validate_serial(user_input[CONF_INVERTER_SERIAL])
                model = await get_inverter_model_from_device(user_input[CONF_HOST], user_input[CONF_PORT], user_input[CONF_DONGLE_SERIAL], user_input[CONF_INVERTER_SERIAL])
                if not model:
                    errors["base"] = "model_fetch_failed"
                else:
                    # Merge the existing data with the new user input
                    new_data = self.config_entry.data.copy()
                    new_data.update(user_input)
                    new_data["model"] = model
                    
                    # Update the config entry with the new data and reload the integration
                    self.hass.config_entries.async_update_entry(self.config_entry, data=new_data, options={})
                    await self.hass.config_entries.async_reload(self.config_entry.entry_id)
                    # Finish the flow
                    return self.async_create_entry(title="", data={})
            except vol.Invalid:
                errors["base"] = "invalid_serial"
        
        # Get the current configuration to use as the default values in the form
        current_config = {**self.config_entry.data, **self.config_entry.options}
        
        # Define the schema for the options form
        options_schema = vol.Schema({
            vol.Required(CONF_HOST): str,
            vol.Required(CONF_PORT): int,
            vol.Required(CONF_DONGLE_SERIAL): str,
            vol.Required(CONF_INVERTER_SERIAL): str,
            vol.Required(CONF_POLL_INTERVAL): vol.All(int, vol.Range(min=2, max=600)),
            vol.Optional(CONF_ENTITY_PREFIX): str,
            vol.Required(CONF_RATED_POWER): vol.All(int, vol.Range(min=1000, max=100000)),
            vol.Optional(CONF_READ_ONLY): bool,
        })

        # Show the options form, pre-filled with the current settings
        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(options_schema, current_config),
            errors=errors,
        )