from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.core import callback

from .const import *
from .entity_descriptions.switch_types import SWITCH_TYPES

async def async_setup_entry(hass, entry, async_add_entities):
    entity_prefix = entry.data.get(CONF_ENTITY_PREFIX, DEFAULT_ENTITY_PREFIX)
    data_store = hass.data[DOMAIN][entry.entry_id]["registers"]

    entities = [
        ModbusBridgeSwitch(entry, desc, entity_prefix, data_store)
        for desc in SWITCH_TYPES
    ]
    async_add_entities(entities)

class ModbusBridgeSwitch(SwitchEntity):
    def __init__(self, entry, desc, entity_prefix, data_store):
        self._entry = entry
        self._desc = desc
        self._entity_prefix = entity_prefix
        self._data_store = data_store
        self._unsub_dispatcher = None
        self._register = desc["register"]
        self._register_type = desc.get("register_type", "hold")
        self._extract = desc["extract"]
        self._compose = desc["compose"]
        self._attr_name = f"{entity_prefix} {desc['name']}"
        self._attr_icon = desc.get("icon")
        self._attr_device_class = desc.get("device_class")
        self._attr_unique_id = f"{entity_prefix}_{desc['register']}_{desc['name'].replace(' ', '_').lower()}"

        self._attr_entity_registry_enabled_default = desc.get("enabled", True)
        self._attr_entity_registry_visible_default = desc.get("visible", True)

    async def async_added_to_hass(self) -> None:
        """Connect to dispatcher."""
        
        # Default to the input signal. This correctly handles our calculated sensor,
        # which depends only on input registers.
        signal = SIGNAL_INPUT_REGISTERS_UPDATED
        
        # If the register_type is 'hold', listen to the hold signal instead.
        if self._register_type == "hold":
            signal = SIGNAL_HOLD_REGISTERS_UPDATED
        
        self._unsub_dispatcher = async_dispatcher_connect(
            self.hass,
            signal,
            self._handle_update,
        )

    async def async_will_remove_from_hass(self):
        if self._unsub_dispatcher:
            self._unsub_dispatcher()
            self._unsub_dispatcher = None

    @callback
    def _handle_update(self, entry_id: str) -> None:
        """Handle the single 'data is ready' signal and schedule an update."""
        if self._entry.entry_id == entry_id:
            self.async_write_ha_state()

    @property
    def is_on(self):
        registers = self._data_store.get(self._register_type, {})
        value = registers.get(self._register)
        if value is None:
            return False
        return bool(self._extract(value))

    async def async_turn_on(self, **kwargs):
        await self._set_bit_value(1)

    async def async_turn_off(self, **kwargs):
        await self._set_bit_value(0)

    async def _set_bit_value(self, value):
        from .services.push_data import write_register
        registers = self._data_store.get(self._register_type, {})
        orig = registers.get(self._register, 0)
        reg_val = self._compose(orig, value)
        success = await write_register(self.hass, self._entry, self._register, reg_val)
        if success:
            registers[self._register] = reg_val
            self.async_write_ha_state()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title if hasattr(self._entry, "title") else INTEGRATION_TITLE,
            "manufacturer": "LUXPower",
            "model": self._entry.data.get("model") or "Unknown"
        }