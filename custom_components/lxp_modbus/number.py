from homeassistant.components.number import NumberEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, CONF_ENTITY_PREFIX, DEFAULT_ENTITY_PREFIX, SIGNAL_REGISTER_UPDATED, INTEGRATION_TITLE
from .entity_descriptions.number_types import NUMBER_TYPES
from .services.push_data import write_register

async def async_setup_entry(hass, entry, async_add_entities):
    entity_prefix = entry.data.get(CONF_ENTITY_PREFIX, DEFAULT_ENTITY_PREFIX)
    data_store = hass.data[DOMAIN][entry.entry_id]["registers"]

    entities = [
        ModbusBridgeNumber(
            entry, desc, entity_prefix, data_store
        )
        for desc in NUMBER_TYPES
    ]
    async_add_entities(entities)

class ModbusBridgeNumber(NumberEntity):
    def __init__(self, entry, desc, entity_prefix, data_store):
        self._entry = entry
        self._desc = desc
        self._entity_prefix = entity_prefix
        self._data_store = data_store

        self._attr_name = f"{entity_prefix} {desc['name']}"
        self._attr_unique_id = f"{entity_prefix}_{desc['register']}_{desc['name'].replace(' ', '_').lower()}"
        self._attr_native_unit_of_measurement = desc.get("unit")
        self._attr_icon = desc.get("icon")
        self._register_type = desc.get("register_type", "hold")
        self._register = desc["register"]
        self._attr_native_min_value = desc.get("min", 0)
        self._attr_native_max_value = desc.get("max", 100)
        self._attr_native_step = desc.get("step", 1)
        self._multiplier = desc.get("multiplier", 1)

        self._attr_entity_registry_enabled_default = desc.get("enabled", True)
        self._attr_entity_registry_visible_default = desc.get("visible", True)

        self._unsub_dispatcher = None

    async def async_added_to_hass(self):
        self._unsub_dispatcher = async_dispatcher_connect(
            self.hass,
            SIGNAL_REGISTER_UPDATED,
            self._handle_register_update
        )

    async def async_will_remove_from_hass(self):
        if self._unsub_dispatcher:
            self._unsub_dispatcher()
            self._unsub_dispatcher = None

    def _handle_register_update(self, entry_id, register_type, reg, new_val):
        if (
            entry_id == self._entry.entry_id
            and register_type == self._register_type
            and reg == self._register
        ):
            self.hass.loop.call_soon_threadsafe(self.async_write_ha_state)

    async def async_set_native_value(self, value):
        value_to_write = int(value * self._multiplier)
        success = await write_register(self.hass, self._entry, self._register, value_to_write)
        if success:
            # Optimistically update state, or rely on poller to refresh
            self._data_store.get(self._register_type, {})[self._register] = value_to_write
            self.async_write_ha_state()

    @property
    def native_value(self):
        registers = self._data_store.get(self._register_type, {})
        value = registers.get(self._register)
        if value is None:
            return None
        
        scaled_value = value / self._multiplier

        # Check if the result is a whole number (e.g., 30.0)
        if scaled_value == int(scaled_value):
            return int(scaled_value)  # Return it as an integer (e.g., 30)
        
        # Otherwise, return it as a decimal
        return scaled_value

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title if hasattr(self._entry, "title") else INTEGRATION_TITLE,
            "manufacturer": "LUXPower",
            "model": self._entry.data.get("model") or "Unknown"
        }