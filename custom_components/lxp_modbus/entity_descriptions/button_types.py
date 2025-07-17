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
    },
]