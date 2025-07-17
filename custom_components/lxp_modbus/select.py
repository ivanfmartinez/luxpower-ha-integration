from homeassistant.components.select import SelectEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, CONF_ENTITY_PREFIX, DEFAULT_ENTITY_PREFIX, SIGNAL_REGISTER_UPDATED
from .entity_descriptions.selectbox_types import SELECTBOX_TYPES

import logging
_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    entity_prefix = entry.data.get(CONF_ENTITY_PREFIX, DEFAULT_ENTITY_PREFIX)
    data_store = hass.data[DOMAIN][entry.entry_id]["registers"]

    entities = [
        ModbusBridgeSelectEntity(entry, desc, entity_prefix, data_store)
        for desc in SELECTBOX_TYPES
    ]
    async_add_entities(entities)

class ModbusBridgeSelectEntity(SelectEntity):
    def __init__(self, entry, desc, entity_prefix, data_store):
        self._entry = entry
        self._desc = desc
        self._entity_prefix = entity_prefix
        self._data_store = data_store

        self._register = desc["register"]
        self._register_type = desc.get("register_type", "hold")
        self._extract = desc["extract"]
        self._compose = desc["compose"]
        self._options = [v for v in desc["options"].values()]
        self._option_keys = {v: k for k, v in desc["options"].items()}
        self._attr_name = f"{entity_prefix} {desc['name']}"
        self._attr_unique_id = f"{entity_prefix}_{desc['register']}_{desc['name'].replace(' ', '_').lower()}"
        self._attr_icon = desc.get("icon")
        self._unsub_dispatcher = None
        
        self._attr_entity_registry_enabled_default = desc.get("enabled", True)
        self._attr_entity_registry_visible_default = desc.get("visible", True)

    async def async_added_to_hass(self):
        self._unsub_dispatcher = async_dispatcher_connect(
            self.hass, SIGNAL_REGISTER_UPDATED, self._handle_register_update
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
            self.async_write_ha_state()

    async def async_select_option(self, option):
        from .services.push_data import write_register
        idx = self._option_keys.get(option)
        if idx is None:
            return
        # Compose the register value for just this option (preserve bits if needed)
        registers = self._data_store.get(self._register_type, {})
        orig = registers.get(self._register, 0)
        reg_val = self._compose(orig, idx)
        success = await write_register(self.hass, self._entry, self._register, reg_val)
        if success:
            registers[self._register] = reg_val
            self.async_write_ha_state()

    @property
    def options(self):
        return self._options

    @property
    def current_option(self):
        registers = self._data_store.get(self._register_type, {})
        value = registers.get(self._register)
        if value is None:
            return None
        idx = self._extract(value)
        return self._desc["options"].get(idx)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title if hasattr(self._entry, "title") else "My Modbus Bridge",
            "manufacturer": "LUXPower",
            "model": self._entry.data.get("model") or "Unknown"
        }