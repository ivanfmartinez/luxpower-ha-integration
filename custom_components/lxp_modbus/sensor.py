from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, CONF_ENTITY_PREFIX, DEFAULT_ENTITY_PREFIX, SIGNAL_REGISTER_UPDATED, INTEGRATION_TITLE
from .entity_descriptions.sensor_types import SENSOR_TYPES

async def async_setup_entry(hass, entry, async_add_entities):
    entity_prefix = entry.data.get(CONF_ENTITY_PREFIX, DEFAULT_ENTITY_PREFIX)
    data_store = hass.data[DOMAIN][entry.entry_id]["registers"]

    entities = [
        ModbusBridgeSensor(
            entry, desc, entity_prefix, data_store
        )
        for desc in SENSOR_TYPES
    ]
    async_add_entities(entities)

class ModbusBridgeSensor(SensorEntity):
    def __init__(self, entry, desc, entity_prefix, data_store):
        self._entry = entry
        self._desc = desc
        self._entity_prefix = entity_prefix
        self._data_store = data_store

        self._attr_name = f"{entity_prefix} {desc['name']}"
        self._attr_icon = desc.get("icon")
        self._extract = desc["extract"]
        self._register_type = desc.get("register_type", "input")

        if self._register_type  == "calculated":
            # For calculated sensors, build the ID from its dependencies and name
            dependencies_str = '_'.join(map(str, self._desc['depends_on']))
            self._attr_unique_id = f"{entity_prefix}_{self._register_type}_{dependencies_str}_{self._desc['name'].replace(' ', '_').lower()}"
            
            # Set attributes for calculated sensors
            self._register = None # Calculated sensors don't have a single primary register
        else:
            # For standard sensors, build the ID from its 'register'
            self._register = self._desc["register"]
            self._attr_unique_id = f"{entity_prefix}_{desc['register']}_{desc['name'].replace(' ', '_').lower()}"

        if "options" in self._desc:
            # This is a text sensor
            self._attr_device_class = None
            self._attr_native_unit_of_measurement = None
        else:
            # This is a numerical sensor
            self._attr_device_class = desc.get("device_class")
            self._attr_native_unit_of_measurement = desc.get("unit")



        self._attr_entity_registry_enabled_default = desc.get("enabled", True)
        self._attr_entity_registry_visible_default = desc.get("visible", True)

    async def async_added_to_hass(self):
        self._unsub_dispatcher = async_dispatcher_connect(
            self.hass,
            SIGNAL_REGISTER_UPDATED,
            self._handle_register_update,
        )

    async def async_will_remove_from_hass(self):
        if hasattr(self, "_unsub_dispatcher") and self._unsub_dispatcher:
            self._unsub_dispatcher()
            self._unsub_dispatcher = None

    def _handle_register_update(self, entry_id, register_type, reg, new_val):

        if entry_id != self._entry.entry_id:
            return

        update = False
        
        if self._desc.get("type") == "calculated":
            if reg in self._desc.get("depends_on", []):
                update = True
        elif register_type == self._register_type and reg == self._register:
            update = True
        
        if update:
            self.hass.loop.call_soon_threadsafe(self.async_write_ha_state)

    @property
    def native_value(self):
        if self._register_type  == "calculated":
            calculation_func = self._desc["extract"]
            # Pass the necessary data stores to the calculation function
            return calculation_func(self._data_store.get("input", {}), self._entry)

        # Get the current register set ('input' or 'hold')
        registers = self._data_store.get(self._register_type, {})
        value = registers.get(self._register)
        if value is None:
            return None
        
        raw_val = self._desc["extract"](value)

        if "options" in self._desc:
            options_map = self._desc["options"]
            default_text = self._desc.get("default", "Unknown")
            return options_map.get(raw_val, default_text)
        
        # Otherwise, treat it as a numerical sensor and apply scaling
        else:
            scale = self._desc.get("scale", 1.0)
            scaled_value = raw_val * scale

            if raw_val == int(scaled_value):
                return int(scaled_value)  # Return it as an integer (e.g., 30)
        
            # Otherwise, return it as a decimal
            return scaled_value

    @property
    def extra_state_attributes(self):
        return {
            "register": self._register,
            "register_type": self._register_type,
        }

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title if hasattr(self._entry, "title") else INTEGRATION_TITLE,
            "manufacturer": "LUXPower",
            "model": self._entry.data.get("model") or "Unknown"
        }