from ..constants.hold_registers import *
from ..utils import get_bits, set_bits

BUTTON_TYPES = [
    # Register 11: H_RESET_SETTINGS
    {
        "name": "Reboot Inverter",
        "register": H_RESET_SETTINGS, # 11
        "register_type": "hold",
        "press": lambda orig, value: set_bits(orig, 7, 1, value),
        "icon": "mdi:restart-alert",
        "enabled": True,
        "visible": True,
        "master_only": False,
    },
    {
        "name": "Clear Detected Phases",
        "register": H_SET_COMPOSED_PHASE,
        "register_type": "hold",
        "icon": "mdi:eraser",
        # The press action ignores the original value and always writes 0
        "press": lambda orig: 0,
        "enabled": True,
        "visible": True,
        "master_only": False,
        "device_group": "Grid",
    },
]