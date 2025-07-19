def decode_model_from_registers(registers: dict) -> str:
    """
    Decode inverter model from 2 HOLD registers (7 and 8).
    Each register holds 2 ASCII chars: HighByte and LowByte.
    """
    chars = []
    for reg in (7, 8):
        value = registers.get(reg, 0)
        chars.append(chr((value >> 8) & 0xFF))  # High byte
        chars.append(chr(value & 0xFF))         # Low byte
    return ''.join(chars).strip('\x00').strip()

def get_bits(value: int, start_bit: int, bit_count: int) -> int:
    """Extract bit field from value."""
    mask = (1 << bit_count) - 1
    return (value >> start_bit) & mask

def set_bits(orig_value: int, start_bit: int, bit_count: int, new_bits: int) -> int:
    """Set bit field in orig_value to new_bits, return new integer value."""
    mask = (1 << bit_count) - 1
    # Clear bits in original value
    cleared = orig_value & ~(mask << start_bit)
    # Set new bits
    return cleared | ((new_bits & mask) << start_bit)

def decode_bitmask_to_string(value, code_map, default_string="OK"):
    """Decodes a 32-bit bitmask into a comma-separated string."""
    if value is None or value == 0:
        return default_string
    active_messages = []
    for bit, message in code_map.items():
        if (value >> bit) & 1:
            active_messages.append(message)
    return ", ".join(active_messages) if active_messages else default_string