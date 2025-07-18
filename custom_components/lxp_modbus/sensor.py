import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import *
from .entity import ModbusBridgeEntity
from .entity_descriptions.sensor_types import SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up sensor entities from a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    entity_prefix = hass.data[DOMAIN][entry.entry_id]['settings'].get(CONF_ENTITY_PREFIX, DEFAULT_ENTITY_PREFIX)
    api_client = hass.data[DOMAIN][entry.entry_id]["api_client"]

    entities = [
        ModbusBridgeSensor(coordinator, entry, desc, entity_prefix, api_client)
        for desc in SENSOR_TYPES
    ]
    async_add_entities(entities)

class ModbusBridgeSensor(ModbusBridgeEntity, SensorEntity):
    """Represents a sensor entity that gets its data from the coordinator."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry, desc: dict, entity_prefix: str, api_client):
        """Initialize the sensor."""
        # Call the parent __init__ to handle all the common setup
        super().__init__(coordinator, entry, desc, entity_prefix, api_client)
        
        # Now, just set up the sensor-specific attributes
        self._register_type = self._desc.get("register_type", "input")
        if "options" in self._desc:
            # This is a text sensor
            self._attr_device_class = None
            self._attr_native_unit_of_measurement = None
        else:
            # This is a numerical sensor
            self._attr_device_class = self._desc.get("device_class")
            self._attr_native_unit_of_measurement = self._desc.get("unit")

    @property
    def native_value(self):
        """Return the state of the sensor."""
        
        # --- MODIFICATION START ---
        # Data is now fetched from self.coordinator.data instead of the old data_store.
        
        # First, check if the coordinator has any data yet.
        if not self.coordinator.data:
            return None

        # If it's a calculated sensor, pass the relevant data to its function
        if self._desc.get("register_type") == "calculated":
            # --- NEW DEBUG LOGGING START ---
            input_data = self.coordinator.data.get("input", {})
            entry_data = self._entry.data

            calculation_func = self._desc["extract"]
            return calculation_func(input_data, self._entry)

        # For standard register-based sensors:
        registers = self.coordinator.data.get(self._register_type, {})
        value = registers.get(self._register)
        
        if value is None:
            return None

        # Extract the raw value using the lambda from the description
        raw_val = self._desc["extract"](value)

        if "options" in self._desc:
            # Handle text sensors that map a value to a string
            return self._desc["options"].get(raw_val, self._desc.get("default", "Unknown"))
        else:
            # Handle numerical sensors by applying the scale
            scale = self._desc.get("scale", 1.0)
            scaled_value = raw_val * scale
            # Return a clean int if it's a whole number, otherwise a float
            return int(scaled_value) if scaled_value == int(scaled_value) else scaled_value