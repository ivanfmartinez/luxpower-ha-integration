"""Base class for LuxPower Modbus entities."""
import logging  # Add this import
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity

from .const import DOMAIN, INTEGRATION_TITLE

_LOGGER = logging.getLogger(__name__)

class ModbusBridgeEntity(CoordinatorEntity):
    """A base class for all LuxPower Modbus entities."""

    def __init__(self, coordinator: DataUpdateCoordinator, entry, desc: dict, entity_prefix: str, api_client):

        """Initialize the entity."""
        super().__init__(coordinator)
        self._entry = entry
        self._desc = desc
        self._entity_prefix = entity_prefix
        self._api_client = api_client

        # Set common attributes
        self._attr_name = f"{entity_prefix} {self._desc['name']}"
        self._attr_entity_registry_enabled_default = self._desc.get("enabled", True)
        self._attr_entity_registry_visible_default = self._desc.get("visible", True)
        
        # Generate unique ID based on whether it's a register-based or calculated entity
        if self._desc.get("register_type") == "calculated":
            dependencies_str = '_'.join(map(str, self._desc['depends_on']))
            self._attr_unique_id = f"{entity_prefix}_{dependencies_str}_{self._desc['name'].replace(' ', '_').lower()}"
            self._register = None
            self._register_type = "calculated"
        else:
            self._register = self._desc["register"]
            self._register_type = self._desc.get("register_type")
            self._attr_unique_id = f"{entity_prefix}_{self._register}_{self._desc['name'].replace(' ', '_').lower()}"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self._register_type == "calculated":
            return {"dependencies": self._desc.get("depends_on")}
        return {
            "register": self._register,
            "register_type": self._register_type,
        }

    
    @property
    def device_info(self):
        """Return device information for all entities."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": self._entry.title or INTEGRATION_TITLE,
            "manufacturer": "LUXPower",
            "model": self._entry.data.get("model") or "Unknown"
        }