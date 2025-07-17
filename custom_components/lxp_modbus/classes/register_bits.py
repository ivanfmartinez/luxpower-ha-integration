class RegisterBits:
    @staticmethod
    def get_bits(value: int, start_bit: int, bit_count: int) -> int:
        mask = (1 << bit_count) - 1
        return (value >> start_bit) & mask

    @staticmethod
    def set_bits(value: int, start_bit: int, bit_count: int, new_bits: int) -> int:
        mask = ((1 << bit_count) - 1) << start_bit
        return (value & ~mask) | ((new_bits << start_bit) & mask)
