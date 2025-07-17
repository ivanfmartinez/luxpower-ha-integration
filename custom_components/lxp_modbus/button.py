from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, CONF_ENTITY_PREFIX, DEFAULT_ENTITY_PREFIX, SIGNAL_REGISTER_UPDATED
from .entity_descriptions.button_types import BUTTON_TYPES

async def async_setup_entry(hass, entry, async_add_entities):
    entity_prefix = entry.data.get(CONF_ENTITY_PREFIX, DEFAULT_ENTITY_PREFIX)
    data_store = hass.data[DOMAIN][entry.entry_id]["registers"]

    entities = [
        ModbusBridgeButtonEntity(entry, desc, entity_prefix, data_store)
        for desc in BUTTON_TYPES
    ]
    async_add_entities(entities)

class ModbusBridgeButtonEntity(ButtonEntity):
    def __init__(self, entry, desc, entity_prefix, data_store):
        self._entry = entry
        self._desc = desc
        self._entity_prefix = entity_prefix
        self._data_store = data_store

        self._register = desc["register"]
        self._register_type = desc.get("register_type", "hold")
        #self._extract = desc["extract"]
        self._press = desc["press"]
        self._icon = desc.get("icon")
        self._attr_name = f"{entity_prefix} {desc['name']}"
        self._attr_unique_id = f"{entity_prefix}_{desc['register']}_{desc['name'].replace(' ', '_').lower()}"
        self._attr_icon = self._icon
        self._unsub_dispatcher = None

    async def async_will_remove_from_hass(self):
        if self._unsub_dispatcher:
            self._unsub_dispatcher()
            self._unsub_dispatcher = None

    async def async_press(self):
        from .services.push_data import write_register
        registers = self._data_store.get(self._register_type, {})
        orig = registers.get(self._register, 0)
        reg_val = self._press(orig)
        success = await write_register(self.hass, self._entry, self._register, reg_val)
        if success:
            registers[self._register] = reg_val
            self.async_write_ha_state()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title if hasattr(self._entry, "title") else "LuxPower Modbus",
            "manufacturer": "LUXPower",
            "model": self._entry.data.get("model") or "Unknown"
        }