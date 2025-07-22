from ..constants.hold_registers import *

TIME_TYPES = [
    {
        "name": "AC Charging Start Time",
        "register": H_AC_CHARGE_START_TIME, # 68
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-start",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "AC Charging End Time",
        "register": H_AC_CHARGE_END_TIME, # 69
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-end",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "AC Charging Start Time 1",
        "register": H_AC_CHARGE_START_TIME_1, # 70
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-start",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "AC Charging End Time 1",
        "register": H_AC_CHARGE_END_TIME_1, # 71
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-end",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "AC Charging Start Time 2",
        "register": H_AC_CHARGE_START_TIME_2, # 72
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-start",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "AC Charging End Time 2",
        "register": H_AC_CHARGE_END_TIME_2, # 73
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-end",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "AC First Load Start Time",
        "register": H_AC_FIRST_START_TIME, # 152
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-start",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "AC First Load End Time",
        "register": H_AC_FIRST_END_TIME, # 153
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-end",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "AC First Load Start Time 1",
        "register": H_AC_FIRST_START_TIME_1, # 154
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-start",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "AC First Load End Time 1",
        "register": H_AC_FIRST_END_TIME_1, # 155
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-end",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Peak Shaving Start Time",
        "register": H_PEAK_SHAVING_START_TIME, # 209
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-start",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Peak Shaving End Time",
        "register": H_PEAK_SHAVING_END_TIME, # 210
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-end",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Peak Shaving Start Time 1",
        "register": H_PEAK_SHAVING_START_TIME_1, # 211
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-start",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Peak Shaving End Time 1",
        "register": H_PEAK_SHAVING_END_TIME_1, # 212
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:clock-end",
        "enabled": True,
        "visible": True,
    },

    # --- New Time Entities from 2025-06-14 Documentation ---
    {
        "name": "Generator Start Time",
        "register": H_GEN_START_TIME,
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:engine-outline",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Generator End Time",
        "register": H_GEN_END_TIME,
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:engine-off-outline",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Generator Start Time 1",
        "register": H_GEN_START_TIME_1,
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:engine-outline",
        "enabled": True,
        "visible": True,
    },
    {
        "name": "Generator End Time 1",
        "register": H_GEN_END_TIME_1,
        "register_type": "hold",
        "extract": lambda reg: (reg & 0xFF, (reg >> 8) & 0xFF),
        "compose": lambda hour, minute: (hour & 0xFF) | ((minute & 0xFF) << 8),
        "icon": "mdi:engine-off-outline",
        "enabled": True,
        "visible": True,
    },
]