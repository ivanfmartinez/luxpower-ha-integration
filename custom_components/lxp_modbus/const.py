from typing import Final
from homeassistant.const import Platform

DOMAIN = "my_modbus_bridge"

PLATFORMS: Final = [
    Platform.SENSOR,
    Platform.NUMBER,
    Platform.TIME,
    Platform.SELECT,
    Platform.BUTTON,
    Platform.SWITCH,
]

CONF_HOST = "host"
CONF_PORT = "port"
CONF_DONGLE_SERIAL = "dongle_serial"
CONF_INVERTER_SERIAL = "inverter_serial"
CONF_POLL_INTERVAL = "poll_interval"
CONF_ENTITY_PREFIX = "entity_prefix"
CONF_RATED_POWER = "rated_power"

INTEGRATION_TITLE = "My Modbus Bridge"


DEFAULT_POLL_INTERVAL = 10  # or whatever default you prefer, in seconds
DEFAULT_ENTITY_PREFIX = ""
DEFAULT_RATED_POWER = 5000

REGISTER_BLOCK_SIZE = 125
TOTAL_REGISTERS = 250
RESPONSE_LENGTH_EXPECTED = 287 # for Register block size - 125.

SIGNAL_REGISTER_UPDATED = "my_modbus_bridge_register_updated"