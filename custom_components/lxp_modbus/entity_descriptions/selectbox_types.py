from ..constants.hold_registers import (
    H_SYSTEM_ENABLE_2, H_SET_SYSTEM_TYPE, H_LANGUAGE_AND_DEVICE_TYPE,
    H_PV_INPUT_MODEL, H_REACTIVE_POWER_CMD_TYPE, H_OUTPUT_PRIORITY_CONFIG,
    H_LINE_MODE, H_GRID_TYPE, H_FUNCTION_ENABLE_4, H_LCD_CONFIG,H_EPS_VOLTAGE_SET,
    H_EPS_FREQ_SET
)
from ..utils import get_bits, set_bits

SELECTBOX_TYPES = [
    {
        "name": "AC Charge Type",
        "register": H_SYSTEM_ENABLE_2,   # 120
        "register_type": "hold",
        "extract": lambda reg: get_bits(reg, 1, 3),   # Bits 1-3 [cite: 141]
        "compose": lambda orig, value: set_bits(orig, 1, 3, value),
        "options": {
            0: "Disable", # [cite: 141]
            1: "According to Time", # [cite: 141]
            2: "According to Voltage", # [cite: 141]
            3: "According to SOC", # [cite: 141]
            4: "According to Voltage and Time", # [cite: 141]
            5: "According to SOC and Time", # [cite: 141]
        },
        "icon": "mdi:battery-charging",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Discharge Control Type",
        "register": H_SYSTEM_ENABLE_2,   # 120
        "register_type": "hold",
        "extract": lambda reg: get_bits(reg, 4, 2),   # Bits 4-5 [cite: 141]
        "compose": lambda orig, value: set_bits(orig, 4, 2, value),
        "options": {
            0: "According to Voltage", # [cite: 141]
            1: "According to SOC", # [cite: 141]
            2: "According to Both", # [cite: 141]
        },
        "icon": "mdi:battery-arrow-down",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "On-Grid EOD Type",
        "register": H_SYSTEM_ENABLE_2,   # 120
        "register_type": "hold",
        "extract": lambda reg: get_bits(reg, 6, 1),   # Bit 6 [cite: 141]
        "compose": lambda orig, value: set_bits(orig, 6, 1, value),
        "options": {
            0: "According to Voltage", # [cite: 141]
            1: "According to SOC", # [cite: 141]
        },
        "icon": "mdi:grid",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Generator Charge Type",
        "register": H_SYSTEM_ENABLE_2,   # 120
        "register_type": "hold",
        "extract": lambda reg: get_bits(reg, 7, 1),   # Bit 7 [cite: 141]
        "compose": lambda orig, value: set_bits(orig, 7, 1, value),
        "options": {
            0: "According to Battery Voltage", # [cite: 141]
            1: "According to Battery SOC", # [cite: 141]
        },
        "icon": "mdi:engine",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "System Type",
        "register": H_SET_SYSTEM_TYPE,    # 112
        "register_type": "hold",
        "extract": lambda reg: reg,
        "compose": lambda orig, value: value,
        "options": {
            0: "No parallel (single one)", # [cite: 137]
            1: "Single-phase parallel (primary)", # [cite: 137]
            2: "Secondary", # [cite: 137]
            3: "Three phase parallel (Master)", # [cite: 137]
            4: "2*208 (Master) - for split-phase", # [cite: 137]
        },
        "icon": "mdi:vector-link",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Language",
        "register": H_LANGUAGE_AND_DEVICE_TYPE, # 16
        "register_type": "hold",
        "extract": lambda reg: reg,
        "compose": lambda orig, value: value,
        "options": {
            0: "English", # [cite: 110]
            1: "German", # [cite: 110]
        },
        "icon": "mdi:translate",
        "enabled": False,
        "visible": True,
    },
    {
        "name": "PV Input Model",
        "register": H_PV_INPUT_MODEL, # 20
        "register_type": "hold",
        "extract": lambda reg: reg,
        "compose": lambda orig, value: value,
        "options": {
            0: "No PV", # [cite: 110]
            1: "PV1 in", # [cite: 110]
            2: "PV2 in", # [cite: 110]
            3: "PV3 in", # [cite: 110]
            4: "PV1 & PV2 in", # [cite: 110]
            5: "PV1 & PV3 in", # [cite: 110]
            6: "PV2 & PV3 in", # [cite: 110]
            7: "PV1 & PV2 & PV3 in", # [cite: 110]
        },
        "icon": "mdi:solar-panel",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Reactive Power Command Type",
        "register": H_REACTIVE_POWER_CMD_TYPE, # 59
        "register_type": "hold",
        "extract": lambda reg: reg,
        "compose": lambda orig, value: value,
        "options": {
            0: "Unit power factor", # [cite: 124]
            1: "Fixed PF", # [cite: 124]
            2: "Default PF curve (Q(P))", # [cite: 124]
            3: "Custom PF curve", # [cite: 124]
            4: "Capacitive reactive power percentage", # [cite: 124]
            5: "Inductive reactive power percentage", # [cite: 124]
            6: "Q(V) curve", # [cite: 124]
            7: "Q(V) Dynamic", # [cite: 124]
        },
        "icon": "mdi:flash",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Output Priority Config",
        "register": H_OUTPUT_PRIORITY_CONFIG, # 145
        "register_type": "hold",
        "extract": lambda reg: reg,
        "compose": lambda orig, value: value,
        "options": {
            0: "Battery First", # [cite: 151]
            1: "PV First", # [cite: 151]
            2: "AC First", # [cite: 151]
        },
        "icon": "mdi:power-plug",
        "enabled": False,
        "visible": True,
    },
    {
        "name": "Line Mode",
        "register": H_LINE_MODE, # 146
        "register_type": "hold",
        "extract": lambda reg: reg,
        "compose": lambda orig, value: value,
        "options": {
            0: "APL (Appliance)", # [cite: 151]
            1: "UPS (Uninterruptible Power Supply)", # [cite: 151]
            2: "GEN (Generator)", # [cite: 151]
        },
        "icon": "mdi:power-settings",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Grid Type",
        "register": H_GRID_TYPE, # 205
        "register_type": "hold",
        "extract": lambda reg: reg,
        "compose": lambda orig, value: value,
        "options": {
            0: "Split Phase 240V/120V", # [cite: 160]
            1: "3-Phase 208V/120V", # [cite: 160]
            2: "Single Phase 240V", # [cite: 160]
            3: "Single Phase 230V", # [cite: 160]
            4: "Split Phase 200V/100V", # [cite: 160]
        },
        "icon": "mdi:transmission-tower",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Smart Load Enable",
        "register": H_FUNCTION_ENABLE_4, # 179
        "register_type": "hold",
        "extract": lambda reg: get_bits(reg, 13, 1), # Bit 13 [cite: 156]
        "compose": lambda orig, value: set_bits(orig, 13, 1, value),
        "options": {
            0: "Generator", # [cite: 156]
            1: "Smart Load", # [cite: 156]
        },
        "icon": "mdi:home-lightning-bolt",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "LCD Screen Type",
        "register": H_LCD_CONFIG, # 224
        "register_type": "hold",
        "extract": lambda reg: get_bits(reg, 8, 1), # Bit 8 [cite: 162]
        "compose": lambda orig, value: set_bits(orig, 8, 1, value),
        "options": {
            0: "Screen 'B' size", # [cite: 162]
            1: "Screen 'S' size", # [cite: 162]
        },
        "icon": "mdi:monitor",
        "enabled": False,
        "visible": True,
    },
    {
        "name": "EPS Voltage Set",
        "register": H_EPS_VOLTAGE_SET,
        "register_type": "hold",
        "icon": "mdi:power-socket-us",
        "extract": lambda value: value,
        "compose": lambda orig, value: value,
        "options": {
            208: "208 V",
            220: "220 V",
            230: "230 V",
            240: "240 V",
            277: "277 V"
        },
        "enabled": True,
        "visible": True,
    },
    {
        "name": "EPS Frequency Set",
        "register": H_EPS_FREQ_SET,
        "register_type": "hold",
        "icon": "mdi:sine-wave",
        "extract": lambda value: value,
        "compose": lambda orig, value: value,
        "options": {
            50: "50 Hz",
            60: "60 Hz"
        },
        "enabled": True,
        "visible": True,
    },
]